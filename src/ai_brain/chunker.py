from abc import ABC, abstractmethod
from langchain.docstore.document import Document as lc_Document
from ai_commons.apiModelsSearch import Document, Chunk
from langchain.text_splitter import CharacterTextSplitter
from typing import Any, Dict, List
from dotenv import load_dotenv
import logging
from utils.robust_jsonify import robust_jsonify
import os
from pydantic import validate_call

load_dotenv()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

CHUNKER_SEPARATOR = os.environ.get('CHUNKER_SEPARATOR', '\n')
if CHUNKER_SEPARATOR == '\\n':
    CHUNKER_SEPARATOR = '\n'
CHUNKER_CHUNK_SIZE = int(os.environ.get('CHUNKER_CHUNK_SIZE', 256))
CHUNKER_CHUNK_OVERLAP = int(os.environ.get('CHUNKER_CHUNK_OVERLAP', 20))


class Chunker(ABC):

    def __init__(self, separator: str = CHUNKER_SEPARATOR, chunk_size: int = CHUNKER_CHUNK_SIZE, chunk_overlap: int = CHUNKER_CHUNK_OVERLAP):
        logger.info(f"Chunker initialized with separator: {
                    repr(separator)}, chunk_size: {chunk_size} [{type(chunk_size)}], chunk_overlap: {chunk_overlap} [{type(chunk_overlap)}]")
        self.text_splitter = CharacterTextSplitter(
            separator=separator,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    @abstractmethod
    def chunkify(self, document: Document) -> List[Chunk]:
        pass

    @abstractmethod
    def chunkify_documents(self, documents: List[Document]) -> List[Document]:
        pass

    @abstractmethod
    def get_params(self) -> Dict[str, Any]:
        pass
