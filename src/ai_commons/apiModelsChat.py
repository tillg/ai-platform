from typing import Any, Dict, List, Optional
import uuid
from pydantic import BaseModel
from langchain.docstore.document import Document as lc_Document
import os
from utils.dict2file import write_dict_to_file, read_dict_from_file

class Message(BaseModel):
    content: str
    role: str 
    inner_working: Optional[Dict[str, Any]] = None

class ChatRequest(BaseModel):
    messages: list[Message]
    context: Optional[dict] = None
    model: Optional[str] = None

    def to_dict(self):
        dict = {}
        if self.model is not None:  # Only include model if it's not None
            dict['model'] = self.model
        dict['messages'] = [message.model_dump() for message in self.messages]
        return dict


