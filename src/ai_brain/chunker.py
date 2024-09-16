from abc import ABC, abstractmethod
from ai_commons.apiModelsSearch import Document, Chunk
from typing import Any, Dict, List
import logging
import os
from pydantic import validate_call
from utils.dict2file import write_dict_to_file
from utils.utils import get_files, get_now_as_string
from tqdm import tqdm

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)

DEFAULT_INDEX_FILENAME = "_chunk_index.json"
DEFAULT_FILES_TO_IGNORE = ["*index.json"]

class Chunker(ABC):

    @validate_call
    def __init__(self, parameters):
        self.parameters = parameters
        # Check that we have a source & target_dir
        if "target_dir" not in parameters:
            raise ValueError("target_dir is required for Chunker.")
        if "source_dir" not in parameters:
            raise ValueError("source_dir is required for Chunker.")

        # Set some defaults
        self.parameters["index_filename"] = os.path.join(
            self.parameters["target_dir"], DEFAULT_INDEX_FILENAME)
        self.parameters["files_to_ignore"] = parameters.get(
            "files_to_ignore", DEFAULT_FILES_TO_IGNORE)
        self.parameters["delete_target_dir"] = parameters.get("delete_target_dir", True)

    @abstractmethod
    def _chunkify_document(self, document: Document) -> List[Chunk]:
        pass

    def do_chunkify(self):
        self.parameters["last_chunkify"] = get_now_as_string()
        self.parameters["chunkify_state"] = "started"
        write_dict_to_file(dictionary=self.parameters,
                           full_filename=self.parameters["index_filename"])

        source_dir = self.parameters["source_dir"]
        target_dir = self.parameters["target_dir"]
        if self.parameters["delete_target_dir"]:
            for document_file in tqdm(get_files(target_dir), desc=f"Deleting target dir: {target_dir}"):
                os.remove(document_file)
        document_files = get_files(source_dir, patterns_to_ignore=self.parameters["files_to_ignore"], patterns_to_match=["*.json"])
        for document_file in tqdm(document_files, desc=f"Chunkifying files in {source_dir}"):
            doc = Document.from_json_file(document_file)
            chunks = self._chunkify_document(doc)
            for chunk in chunks:
                chunk.write_2_json(target_dir)
        self.parameters["chunkify_state"] = "finished"
        write_dict_to_file(dictionary=self.parameters,
                           full_filename=self.parameters["index_filename"])

    @validate_call
    def _chunkify_documents(self, documents: List[Document]) -> List[Document]:
        chunks = [
            chunk for document in documents for chunk in self.chunkify_document(document)]
        return chunks

    def get_parameters(self) -> Dict[str, Any]:
        return self.parameters

    def get_statistics(self) -> Dict[str, Any]:
        source_dir = self.parameters["source_dir"]
        target_dir = self.parameters["target_dir"]
        document_files = get_files(
            source_dir, patterns_to_ignore=self.parameters["files_to_ignore"], patterns_to_match=["*.json"])
        no_documents = len(document_files)
        chunk_files = get_files(target_dir, patterns_to_ignore=self.parameters["files_to_ignore"], patterns_to_match=["*.json"])
        no_chunks = len(chunk_files)
        return {"no_documents": no_documents, "no_chunks": no_chunks}