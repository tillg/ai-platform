from typing import Any, Dict, List, Optional
import uuid
from pydantic import BaseModel
from langchain.docstore.document import Document as lc_Document
import os
from utils.dict2file import write_dict_to_file, read_dict_from_file


class Message(BaseModel):
    content: str
    role: str = "user"

class ChatRequest(BaseModel):
    messages: list[Message]
    context: Optional[dict] = None


class ChatResponse(BaseModel):
    content: str


