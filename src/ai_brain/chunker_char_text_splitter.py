from langchain.docstore.document import Document as lc_Document
from ai_brain.chunker import Chunker
from ai_commons.api_models import Document, Chunk
from langchain.text_splitter import CharacterTextSplitter
from typing import Any, Dict, List
from dotenv import load_dotenv
import logging
from utils.robust_jsonify import robust_jsonify
import os
import uuid
from pydantic import validate_call

load_dotenv()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
 
CHUNKER_SEPARATOR = os.environ.get('CHUNKER_SEPARATOR', '\n')
if CHUNKER_SEPARATOR == '\\n':
    CHUNKER_SEPARATOR = '\n'
CHUNKER_CHUNK_SIZE = int(os.environ.get('CHUNKER_CHUNK_SIZE', 256))
CHUNKER_CHUNK_OVERLAP = int(os.environ.get('CHUNKER_CHUNK_OVERLAP', 20))


class ChunkerCharacterTextSplitter(Chunker):

    def __init__(self, params: Dict[str, Any]):
        self.original_params = params.copy()
        self.params = params.copy()

        self.params["chunker_type"] = "ChunkerCharacterTextSplitter"
        
        self.separator = params.get("separator", CHUNKER_SEPARATOR)
        self.params["separator"] = self.separator

        self.chunk_size = params.get("chunk_size", CHUNKER_CHUNK_SIZE)
        self.params["chunk_size"] = self.chunk_size

        self.chunk_overlap = params.get("chunk_overlap", CHUNKER_CHUNK_OVERLAP)
        self.params["chunk_overlap"] = self.chunk_overlap

        logger.info(f"ChunkerCharacterTextSplitter initialized with params: {self.params}")
        self.text_splitter = CharacterTextSplitter(
            separator=self.separator,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )


    @validate_call
    def chunkify(self, document: Document) -> List[Chunk]:
        #lc_document = document.to_lc_document()
        try:
            logging.getLogger(
                'langchain_text_splitters.base').setLevel(logging.ERROR)
            lc_chunks = self.text_splitter.create_documents(
                [document.content], metadatas=[document.get_metadata()])
        except Exception as e:
            logger.error(
                f"Error while chunkifying document: {robust_jsonify(document)}")
            logger.error(f"Error: {e}")
            raise
        chunks = []
        for lc_chunk in lc_chunks:
            chunk = Chunk(
                content=lc_chunk.page_content, 
                title=lc_chunk.metadata.get("title", None), 
                uri=lc_chunk.metadata.get("uri", None), 
                original_document_id=document.id
            )
            chunks.append(chunk)
        logger.info(f"Chunkified a document of length {len(document.content)} in {len(chunks)} chunks of length: {
            [len(chunk.content) for chunk in chunks]}")
        return chunks

    @validate_call
    def chunkify_documents(self, documents: List[Document]) -> List[Document]:
        if not isinstance(documents, list):
            logger.error(
                f"documents is not a list: {documents}. It is of type {type(documents)}")
            raise TypeError(f"documents must be a list, not {type(documents)}")
        if not all(isinstance(doc, Document) for doc in documents):
            logger.error(
                f"All elements in list are not instances of Document.")
            raise TypeError(
                "All elements in documents must be instances of Document")

        chunks = [
            chunk for document in documents for chunk in self.chunkify_document(document)]

        return chunks
    
    def get_params(self) -> Dict[str, Any]:
        return self.params
