from abc import ABC, abstractmethod
from ai_commons.apiModelsSearch import Document, Chunk
from typing import Any, Dict, List
from dotenv import load_dotenv
import logging
import os
from pydantic import validate_call

load_dotenv()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Chunker(ABC):

    @validate_call
    def __init__(self, parameters):
        self.parameters = parameters
        # Check that we have a source & target_dir
        if "target_dir" not in parameters:
            raise ValueError("target_dir is required for Brain Scraper.")
        if "source_dir" not in parameters:
            raise ValueError("source_dir is required for Brain Scraper.")

    @abstractmethod
    def _chunkify_document(self, document: Document) -> List[Chunk]:
        pass

    @abstractmethod
    def _chunkify_documents(self, documents: List[Document]) -> List[Document]:
        pass

    def do_chunkify(self):
        source_dir = self.parameters["source_dir"]
        target_dir = self.parameters["target_dir"]
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                if file.endswith(".json"):
                    logger.info(f"Chunking file: {file}")
                    doc = Document.from_json_file(os.path.join(root, file))
                    chunks = self._chunkify_document(doc)
                    for chunk in chunks:
                        chunk.write_2_json(target_dir)

    def get_parameters(self) -> Dict[str, Any]:
        return self.parameters
