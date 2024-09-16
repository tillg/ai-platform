from ai_brain.chunker import Chunker
from ai_commons.apiModelsSearch import Document, Chunk
from ai_commons.constants import CHUNKER_SEPARATOR, CHUNKER_CHUNK_SIZE, CHUNKER_CHUNK_OVERLAP
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
logger.setLevel(logging.WARN)
 

class ChunkerCharacterTextSplitter(Chunker):

    def __init__(self, parameters: Dict[str, Any]):
        super().__init__(parameters=parameters)

        self.parameters["chunker_type"] = "character_text_splitter"
        
        # Complete some parameters with defaults
        self.parameters["separator"] = parameters.get("separator", CHUNKER_SEPARATOR)
        self.parameters["chunk_size"] = parameters.get(
            "chunk_size", CHUNKER_CHUNK_SIZE)
        self.parameters["chunk_overlap"] = parameters.get(
            "chunk_overlap", CHUNKER_CHUNK_OVERLAP)
        logger.info(
            f"character_text_splitter initialized with parameters: {self.parameters}")
        self.text_splitter = CharacterTextSplitter(
            separator=self.parameters["separator"],
            chunk_size=self.parameters["chunk_size"],
            chunk_overlap=self.parameters["chunk_overlap"]
        )

    @validate_call
    def _chunkify_document(self, document: Document) -> List[Chunk]:
        super()._chunkify_document(document)
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

