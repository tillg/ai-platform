# TODO: Review if it still makes sense to keep the documents as files.

from ast import Tuple
from collections import OrderedDict
import os
from uuid import UUID
import chromadb
from chromadb.config import Settings
from tqdm import tqdm
from ai_brain.chunker import Chunker
from ai_brain.chunker_factory import ChunkerFactory
from utils.utils import simplify_text, get_files
from utils.dict2file import write_dict_to_file, read_dict_from_file
import logging
from typing import Any, Dict, List, Union
from ai_commons.apiModelsSearch import Document, Chunk, SearchResultChunksAndDocuments, SearchResult, BrainParameters
from pydantic import field_validator, validate_call
import time
from ai_commons.constants import AI_BRAINS_INDEX_FILE, AI_BRAIN_COLLECTION_NAME
from ai_brain.embedding_function_factory import EmbeddingFunctionFactory
from ai_brain.brain_scraper import BrainScraper
from ai_brain.brain_scraper_factory import BrainScraperFactory

DEFAULT_BATCH_SIZE = 100

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
class Brain:

    @classmethod
    def _read_index_from_file(cls, index_filename):
        logger.info(f"Reading index from file: {index_filename}")
        if os.path.exists(index_filename):
            return read_dict_from_file(full_filename=index_filename)
        return {}

    @classmethod
    def get_brain_parameters_list(cls, brains_index_file: str = AI_BRAINS_INDEX_FILE) -> List[BrainParameters]:
        logger.info(f"get_brain_parameters_list: Reading from brains index file: {
            brains_index_file}")
        brain_dict = read_dict_from_file(full_filename=brains_index_file)
        logger.info(f"Brain dict: {brain_dict}")
        brain_parameters = [BrainParameters(id=brain_id, **brain) for brain_id, brain in brain_dict.items()] 
        return brain_parameters

    @classmethod
    def is_valid_brain_id(cls, brain_id: str, brains_index_file: str = AI_BRAINS_INDEX_FILE) -> bool:
        brain_list = cls.get_brain_parameters_list(brains_index_file)
        for brain in brain_list:
            if brain.id == brain_id:
                return True
        return False

    @classmethod
    def get_brain_by_id(cls, brain_id: str, brains_index_filename: str = AI_BRAINS_INDEX_FILE):
        brain_parameters_list = cls.get_brain_parameters_list(
            brains_index_filename)
        for brain_parameters in brain_parameters_list:
            if brain_parameters.id == brain_id:
                logger.info(f"Brain found: {brain_parameters}")
                return Brain(brain_parameters, id=brain_id)
        logger.error(f"Brain not found: {brain_id}")
        raise ValueError(f"Brain not found: {brain_id}")

    @classmethod
    @validate_call
    def get_default_brain(cls, brains_index_file: str = AI_BRAINS_INDEX_FILE):
        logger.info(f"get_default_brain: Reading from brains index file: {
            brains_index_file}")
        brain_list = cls.get_brain_parameters_list(brains_index_file)
        # This gets the first brain's id
        default_brain_id = next(iter(brain_list)).id
        for brain_parameter in brain_list:
            if getattr(brain_parameter, 'default', False):
                default_brain_id = brain_parameter.id
                break
        return cls.get_brain_by_id(default_brain_id, brains_index_filename=brains_index_file)
    
    @validate_call
    def __init__(self, parameters: BrainParameters, id: str = None):
        self.parameters = parameters.dict()
        logger.info(f"Initializing Brain with parameters: {self.parameters}")

        # Setting some parameters to their defaults in case they are not provided
        self.parameters["id"] = id
        self.parameters["allow_duplicates"] = self.parameters.get('allow_duplicates', False)
        self.parameters["max_no_of_docs"] = self.parameters.get('max_no_of_docs', 0)
        self.parameters["embedding_function"] = self.parameters.get("embedding_function", {})
        
        # Setup Chroma DB
        self.parameters["chroma_directory"] = os.path.join(
            self.parameters["data_directory"], "chroma")
        self.parameters["document_directory"] = os.path.join(
            self.parameters["data_directory"], "documents")
        logging.getLogger("chromadb.api.segment").setLevel(logging.WARNING)
        self.chroma_client = chromadb.PersistentClient(
            path=self.parameters["chroma_directory"], settings=Settings(anonymized_telemetry=False))
        embedding_function = EmbeddingFunctionFactory().create_embedding_function(parameters=self.parameters["embedding_function"])
        self.chroma_collection = self.chroma_client.get_or_create_collection(
            name=AI_BRAIN_COLLECTION_NAME,
            embedding_function=embedding_function)

        # Initialize document index
        self.parameters["index_filename"] = os.path.join(
            self.parameters["data_directory"], "_index.json")
        self.document_index = self._read_index_from_file(
            self.parameters["index_filename"])

        logger.info(f"Brain initialized. Data directory: {
                    self.parameters["data_directory"]}, no of document: {self.number_of_documents()}, no of chunks: {self.number_of_chunks()}")

    
    def get_chunker(self) -> Chunker:
        if (not self.parameters.get("chunker")):
            logger.warning("Chunker not found in brain parameters.")
            return None
        logger.info(f"Creating chunker for brain with parameters: {self.parameters}")
        return ChunkerFactory().create_chunker(parameters=self.parameters["chunker"])
    
    def get_scraper(self) -> BrainScraper:
        if (not self.parameters.get("scraper")):
            logger.warning("Scraper not found in brain parameters.")
            return None
        return BrainScraperFactory().create_brain_scraper(parameters=self.parameters["scraper"])
    
    def get_parameters(self) -> Dict[str, Any]:
        chunker = self.get_chunker()
        if chunker:
            chunker_parameters = chunker.get_parameters()
            self.parameters["chunker"] = chunker_parameters
        scraper = self.get_scraper()
        if scraper:
            scraper_parameters = scraper.get_parameters()
            self.parameters["scraper"] = scraper_parameters
        return self.parameters

    def get_statistics(self) -> Dict[str, Any]:
        stats = {
            "no_of_documents": self.number_of_documents(),
            "no_of_chunks": self.number_of_chunks()
        }
        chunker = self.get_chunker()
        if chunker:
            chunker_statistics = chunker.get_statistics()
            stats["chunker_statistics"] = chunker_statistics
        scraper = self.get_scraper()
        if scraper:
            scraper_statistics = scraper.get_statistics()
            stats["scraper_statistics"] = scraper_statistics
        return stats

    def get_parameters_and_statistics(self) -> Dict[str, Any]:
        parameters = self.get_parameters()
        statistics = self.get_statistics()
        parameters_and_statistics = {
            **parameters, 
            **statistics}
        sorted_parameters_and_statistics = OrderedDict(
            sorted(parameters_and_statistics.items()))
        return sorted_parameters_and_statistics
    
    def number_of_documents(self):
        """Return the number of documents, ensuring the document index is up-to-date."""
        self.document_index = self._read_index_from_file(self.parameters["index_filename"])
        if "_stats" in self.document_index:
            # Exclude the '_stats' entry if present
            return len(self.document_index) - 1
        return len(self.document_index)

    def __str__(self):
        return f"Brain with {self.number_of_documents()} documents and {self.number_of_chunks()} chunks, stored in {self.data_directory} directory."

    def _delete_all_chroma(self):
        self.chroma_client.delete_collection(AI_BRAIN_COLLECTION_NAME)
        self.chroma_collection = self.chroma_client.get_or_create_collection(
            AI_BRAIN_COLLECTION_NAME)
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
        return os.path.join(self.parameters["document_directory"],  id + ".json")

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
                           full_filename=self.parameters["index_filename"])
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

    @validate_call
    def import_chunks(self, chunks: List[Chunk], batch_size=DEFAULT_BATCH_SIZE):
        """ Import chunks into the ChromaDB """
        # TODO: Check if the chunks are already in the collection
        chunks_content = []
        for chunk in chunks:
            chunks_content.append(chunk.content)
        chunks_metadatas = [{"title": chunk.title, "uri": chunk.uri,
                            "original_document_id": chunk.original_document_id} for chunk in chunks]
        chunks_ids = [chunk.id for chunk in chunks]
        for i in tqdm(range(0, len(chunks_content), batch_size), desc=f"Adding {len(chunks)} chunks to ChromaDB in batches of {batch_size}"):
            chunks_content_batch = chunks_content[i:i + batch_size]
            batch_metadatas = chunks_metadatas[i:i + batch_size]
            batch_ids = chunks_ids[i:i + batch_size]

            self.chroma_collection.add(documents=chunks_content_batch,
                                    metadatas=batch_metadatas,
                                    ids=batch_ids)
        logger.info(f"Done: Adding {len(chunks)} chunks to the ChromaDB.")
        return

    #validate_call
    def import_chunks_from_directory(self):
        # Check chunk variable
        if not self.parameters.get("chunks_directory"):
            raise ValueError("chunks_directory not given, brain is not be able to load.")
        
        # Check that the chunks directory exists
        if not os.path.exists(self.parameters["chunks_directory"]):
            logger.error(f"Chunks directory does not exist: {
                         self.parameters["chunks_directory"]}")
            raise FileNotFoundError(f"Chunks directory does not exist: {
                                    self.parameters["chunks_directory"]}")
        # Read chunks from directory
        files = get_files(self.parameters["chunks_directory"], patterns_to_match=[
                          "*.json"], patterns_to_ignore=["*index.json"])
        chunks = []
        for file in tqdm(files, desc=f"Reading chunks from {self.parameters["chunks_directory"]}"):
            chunk = Chunk.from_json_file(file)
            chunks.append(chunk)
        self.import_chunks(chunks)
        return
    
    @validate_call
    def import_document(self, document: Document):
        if self.parameters["max_no_of_docs"] > 0 and self.number_of_documents() >= self.parameters["max_no_of_docs"]:
            logger.warning(
                f"Max number of documents reached: {self.parameters["max_no_of_docs"]}. Document not added.")
            return
        if len(document.content) == 0:
            logger.warning(f"Document with empty content cannot be added. URI: {document.uri}")
            return

        if not self.parameters["allow_duplicates"]:
            if self.is_in_by_uri(document.uri):
                logger.warning(f"Document with URI {
                               document.uri} already exists in the collection.")
                return

        # Add the document to the file store
        document.write_2_json(self.parameters["document_directory"])
        # Add the documen to the index
        self._add_document_to_index(document)
        return

    @validate_call
    def import_documents(self, documents: List[Document], show_progress=True):
        if show_progress:
            documents = tqdm(documents, desc="Importing documents")
        for document in documents:
            self.import_document(document)
        return

    def number_of_chunks(self):
        return self.chroma_collection.count()

    @validate_call
    def search_chunks_by_text(self, query_text: str, n: int = 10) -> SearchResult:
        search_result = SearchResult(inner_working={'vectore store': 'ChromaDB', **self.get_statistics()})
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
