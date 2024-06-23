from typing import Any, Optional
import uuid
from pydantic import BaseModel
from langchain.docstore.document import Document as lc_Document
import os
from utils.dict2file import write_dict_to_file, read_dict_from_file


class BrainInfo(BaseModel):
    title: str = "Brain"
    embedding_model: str
    data_directory: str
    chroma_directory: str
    document_directory: str
    collection_name: str
    no_documents: int
    no_chunks: int

