from ast import Tuple
import os
from uuid import UUID
import chromadb
from chromadb.config import Settings
from tqdm import tqdm
from ai_brain.chunker import Chunker
from utils.utils import simplify_text
from utils.dict2file import write_dict_to_file, read_dict_from_file
import logging
from typing import Any, List
from ai_commons.api_models import Document
from pydantic import field_validator, validate_call

logger = logging.getLogger(__name__)

DATA_DIRECTORY = os.environ.get('DATA_DIRECTORY', "data")
COLLECTION_NAME = os.environ.get('COLLECTION_NAME', 'COLLECTION_NAME')


class Brain:

    @classmethod
    def _read_index_from_file(cls, index_filename):
        logger.info(f"Reading index from file: {index_filename}")
        if os.path.exists(index_filename):
            return read_dict_from_file(full_filename=index_filename)
        return {}

    def __init__(self, data_directory: str = DATA_DIRECTORY, chunker: Chunker = None):
        self.data_directory = data_directory
        self.chroma_directory = os.path.join(self.data_directory, "chroma")
        self.document_directory = os.path.join(
            self.data_directory, "documents")
        self.collection_name = COLLECTION_NAME
        self.chroma_client = chromadb.PersistentClient(
            path=self.chroma_directory, settings=Settings(anonymized_telemetry=False))
        self.chroma_collection = self.chroma_client.get_or_create_collection(
            self.collection_name)
        self.document_index = self._read_index_from_file(
            os.path.join(self.data_directory, "_index.json"))
        self.chunker = chunker
        if self.chunker is None:
            self.chunker = Chunker()

        logger.info(f"Brain initialized. Data path: {
                    self.data_directory}, no of document: {len(self)}, no of chunks: {self.number_of_chunks()}")

    def search_documents_by_text(self, query_text: str):
        return self.chroma_collection.query(query_texts=[query_text])

    def search_documents_by_texts(self, query_texts: List[str]):
        return self.chroma_collection.query(query_texts=query_texts)

    def __len__(self):
        return len(self.document_index)

    @validate_call
    def _id_to_filename(self, id: str):
        return os.path.join(self.document_directory,  id + ".json")

    def _document_to_file(self, document: Document):

        filename = self._id_to_filename(document.id)
        document_dict = document.model_dump()

        # Write to file
        write_dict_to_file(dictionary=document_dict, full_filename=filename)
        return

    def get_document_by_id(self, id: str):
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

    def _write_index_to_file(self):
        filename = os.path.join(self.data_directory, "_index.json")
        write_dict_to_file(dictionary=self.document_index,
                           full_filename=filename)
        return

    def _add_document_to_index(self, document: Document):

        # Transform source to filename
        filename = self._id_to_filename(document.id)

        self.document_index[filename] = document.get_metadata()
        self._write_index_to_file()
        return

    @validate_call
    def add_document(self, document: Document):

        # Add the document to the file store
        self._document_to_file(document)

        # Add the documen to the index
        self._add_document_to_index(document)

        # Chunk the document
        chunks = self.chunker.chunkify(document)

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

    def add_documents(self, documents: List[Document], show_progress=False):
        if show_progress:
            documents = tqdm(documents)
        for document in documents:
            self.add_document(document)
        return

    def number_of_chunks(self):
        return self.chroma_collection.count()

    def _chroma_results_to_chunks_and_scores(self, results: Any):
        return [
            Document(page_content=result[0], metadata=result[1] or {})
            for result in zip(
                results["documents"][0],
                results["metadatas"][0],
            )
        ]

    def get_chunks_by_text_proximity(self, texts: List[str], n_results=10):
        chroma_chunks = self.chroma_collection.query(
            query_texts=texts,
            n_results=n_results
        )
        chunk_documents = self._chroma_results_to_chunks_and_scores(chroma_chunks)
        return chunk_documents
