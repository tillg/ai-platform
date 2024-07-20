from ast import Tuple
import os
from uuid import UUID
import chromadb
from chromadb.config import Settings
from tqdm import tqdm
from ai_brain.chunker import Chunker
from ai_brain.chunker_factory import ChunkerFactory
from utils.utils import simplify_text
from utils.dict2file import write_dict_to_file, read_dict_from_file
import logging
from typing import Any, Dict, List, Union
from ai_commons.api_models import Document, Chunk, SearchResultChunksAndDocuments, SearchResult
from pydantic import field_validator, validate_call
from dotenv import load_dotenv
import time
from ai_commons.constants import AI_BRAINS_DIRECTORY, AI_BRAIN_COLLECTION_NAME

load_dotenv()
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)

class Brain:

    @classmethod
    def _read_index_from_file(cls, index_filename):
        logger.info(f"Reading index from file: {index_filename}")
        if os.path.exists(index_filename):
            return read_dict_from_file(full_filename=index_filename)
        return {}

    @classmethod
    def get_brain_list(cls, brains_directory: str = AI_BRAINS_DIRECTORY, brain_index_filename: str = "brains.json"):
        brain_list = read_dict_from_file(full_filename=os.path.join(
            brains_directory, brain_index_filename))
        return brain_list

    @classmethod
    def get_default_brain(cls, brains_directory: str = AI_BRAINS_DIRECTORY, brain_index_filename: str = "brains.json"):
        brain_list = read_dict_from_file(full_filename=os.path.join(
            brains_directory, brain_index_filename))
        # This gets the first brain's name
        default_brain_id = next(iter(brain_list))
        for brain_id in brain_list:
            if brain_list[brain_id].get("default", False):
                default_brain_id = brain_id
                break
        return cls.get_brain_by_id(default_brain_id, brains_directory, brain_index_filename)
    
    @classmethod
    def get_brain_by_id(cls, brain_id: str, brains_directory: str = AI_BRAINS_DIRECTORY, brain_index_filename: str = "brains.json"):
        brain_list = read_dict_from_file(full_filename=os.path.join(
            brains_directory, brain_index_filename))
        if brain_id in brain_list:
            brain_params = brain_list[brain_id]
            brain_params["data_directory"] = brains_directory
            logger.info(f"Brain found: {brain_params}")
            return Brain(brain_params)
        logger.error(f"Brain not found: {brain_id}")
        raise ValueError(f"Brain not found: {brain_id}")
    
    @classmethod
    def get_env(cls) -> Dict[str, Any]:
        return {
            "AI_BRAINS_DIRECTORY": AI_BRAINS_DIRECTORY,
            "AI_BRAIN_COLLECTION_NAME": AI_BRAIN_COLLECTION_NAME
        }

    def __init__(self, params: Dict[str, Any]):
        self.params = params.copy()
        self.original_params = params.copy()

        if not "data_directory" in params:
            raise ValueError(
                f"Cannot initialize Brain without a 'data_directory' parameter: {params}")
        self.data_directory = params["data_directory"]

        # Check for some params that we absolutely need
        if not "path" in params:
            raise ValueError(
                f"Cannot initialize Brain without a 'path' parameter: {params}")
        self.entire_path = os.path.join(self.data_directory, params["path"])

        self.allow_duplicates = params.get('allow_duplicates', False)
        self.params["allow_duplicates"] = self.allow_duplicates

        self.max_no_of_docs = params.get('max_no_of_docs', 0)
        self.params["max_no_of_docs"] = self.max_no_of_docs

        # Setup Chroma DB
        self.chroma_directory = os.path.join(self.entire_path, "chroma")
        self.document_directory = os.path.join(
            self.entire_path, "documents")
        self.collection_name = AI_BRAIN_COLLECTION_NAME
        self.chroma_client = chromadb.PersistentClient(
            path=self.chroma_directory, settings=Settings(anonymized_telemetry=False))
        self.chroma_collection = self.chroma_client.get_or_create_collection(
            self.collection_name)

        # Initialize document index
        self.index_filename = os.path.join(self.entire_path, "_index.json")
        self.document_index = self._read_index_from_file(self.index_filename)

        # Setup Chunker
        chunker_factory = ChunkerFactory()
        self.chunker = chunker_factory.create_chunker(
            params.get("chunker", {}))
        self.params["chunker"] = self.chunker.get_params()

        logger.info(f"Brain initialized. Data path: {
                    self.data_directory}, no of document: {len(self)}, no of chunks: {self.number_of_chunks()}")

    def get_params(self) -> Dict[str, Any]:
        return self.params

    def get_stats(self) -> Dict[str, Any]:
        stats = {
            "no_of_documents": len(self),
            "no_of_chunks": self.number_of_chunks()
        }
        return stats

    def get_params_and_stats(self) -> Dict[str, Any]:
        params = self.get_params()
        stats = self.get_stats()
        return {**params, **stats}
    
    def __len__(self):
        """Return the number of documents, ensuring the document index is up-to-date."""
        # Assuming 'self.data_directory' holds the path to the directory where '_index.json' is located
        self.document_index = self._read_index_from_file(self.index_filename)
        if "_stats" in self.document_index:
            # Exclude the '_stats' entry if present
            return len(self.document_index) - 1
        return len(self.document_index)

    def __str__(self):
        return f"Brain with {len(self)} documents and {self.number_of_chunks()} chunks, stored in {self.data_directory} directory."

    def _delete_all_chroma(self):
        self.chroma_client.delete_collection(self.collection_name)
        self.chroma_collection = self.chroma_client.get_or_create_collection(
            self.collection_name)
        return

    def _delete_all_documents(self):

        # Convert dict_keys to a list for mutability
        filenames = list(self.document_index.keys())

        # Remove '_stats' from the list if it exists
        if "_stats" in filenames:
            filenames.remove("_stats")
        for filename in filenames:
            os.remove(filename)
            id = self.document_index[filename].get('id')
            self._remove_document_from_index(id)
        return

    def delete_all(self):
        self._delete_all_chroma()
        self._delete_all_documents()
        return

    @validate_call
    def _id_to_filename(self, id: str):
        return os.path.join(self.document_directory,  id + ".json")

    @validate_call
    def get_document_by_id(self, id: str) -> Document:
        # Transform the id to a filename
        filename = self._id_to_filename(id)

        # Check if file exists
        if not os.path.exists(filename):
            logger.error(f"File does not exist: {filename}")
            return None

        # Read file
        document_dict = read_dict_from_file(full_filename=filename)

        # Build Document
        document = Document.model_validate(document_dict)
        return document

    @validate_call
    def get_document_by_uri(self, uri: str) -> Document:
        for id, metadata in self.document_index.items():
            if metadata.get('uri') == uri:
                return self.get_document_by_id(metadata.get('id'))
        return None

    @validate_call
    def is_in_by_uri(self, uri: str) -> bool:
        for id, metadata in self.document_index.items():
            if metadata.get('uri') == uri:
                return True
        return False

    def _write_index_to_file(self):
        write_dict_to_file(dictionary=self.document_index,
                           full_filename=self.index_filename)
        return

    @validate_call
    def _add_document_to_index(self, document: Document):

        # Transform source to filename
        filename = self._id_to_filename(document.id)

        self.document_index[filename] = document.get_metadata()
        self._write_index_to_file()
        return

    @validate_call
    def _remove_document_from_index(self, document_id: str):
        # Transform document ID to filename
        filename = self._id_to_filename(document_id)

        # Check if the document exists in the index and remove it
        if filename in self.document_index:
            del self.document_index[filename]
            self._write_index_to_file()
        else:
            logger.warning(f"Document with ID {
                           document_id} not found in index.")

    def _add_chunks_to_chroma(self, chunks: List[Chunk]):
        # Store the chunks in the collection
        chunks_content = []
        for chunk in chunks:
            chunks_content.append(chunk.content)
        chunks_metadatas = [{"title": chunk.title, "uri": chunk.uri,
                            "original_document_id": chunk.original_document_id} for chunk in chunks]
        chunks_ids = [chunk.id for chunk in chunks]
        self.chroma_collection.add(documents=chunks_content,
                                   metadatas=chunks_metadatas, ids=chunks_ids)
        return

    @validate_call
    def import_document(self, document: Document):
        if self.max_no_of_docs > 0 and len(self) >= self.max_no_of_docs:
            logger.warning(
                f"Max number of documents reached: {self.max_no_of_docs}. Document not added.")
            return
        if document.content is None:
            logger.warning("Document with content None cannot be added.")
            return
        if len(document.content) == 0:
            logger.warning(f"Document with empty content cannot be added. URI: {document.uri}")
            return

        if not self.allow_duplicates:
            if self.is_in_by_uri(document.uri):
                logger.warning(f"Document with URI {
                               document.uri} already exists in the collection.")
                return

        # Add the document to the file store
        document.write_2_file(self.document_directory)
        # Add the documen to the index
        self._add_document_to_index(document)
        return

    @validate_call
    def add_document(self, document: Document):
        self.import_document(document)

        # Chunk the document
        chunks = self.chunker.chunkify(document)

        self._add_chunks_to_chroma(chunks)

        return

    @validate_call
    def add_documents(self, documents: List[Document], show_progress=False):
        if show_progress:
            documents = tqdm(documents)
        for document in documents:
            self.add_document(document)
        return

    def number_of_chunks(self):
        return self.chroma_collection.count()

    def search_chunks_by_text(self, query_text: str, n: int = 10) -> SearchResult:
        search_result = SearchResult(inner_working={'vectore store': 'ChromaDB', 'no of docs': len(
            self), 'no of chunks': self.number_of_chunks()})
        if (query_text is None) or (len(query_text) == 0):
            error_text = "Empty search query."
            logger.warning(error_text)
            search_result.inner_working = {"error": error_text}
            return search_result
        logger.info(f"Searching chunks by text: {query_text}")
        start_time = time.time()
        chroma_chunks = self.chroma_collection.query(
            query_texts=[query_text], n_results=n)
        end_time = time.time()
        duration = int((end_time - start_time)*1000)
        search_result.inner_working.update({"duration (ms)": duration})
        chunks = Chunk.chroma_chunks2chunk_array(
            chroma_chunks, search_term=query_text)
        search_result.search_term = query_text
        result_chunks = SearchResultChunksAndDocuments()
        result_chunks.chunks = chunks
        search_result.result = result_chunks
        logger.info(f"Returning search result: {search_result}")
        return search_result

    def reindex(self):
        logger.info("Re-chunkifying and re-vectorizing all documents.")
        # Delete chunks in chromadb
        self._delete_all_chroma()

        for filename in self.document_index:
            if filename == "_stats":
                continue
            try:
                document_id = self.document_index[filename].get('id')
                document = self.get_document_by_id(document_id)

                # Chunk the document
                chunks = self.chunker.chunkify(document)

                self._add_chunks_to_chroma(chunks)

            except Exception as e:
                logger.error(
                    f"Error re-chunkifying document {filename}: {str(e)}")
                continue

        return
