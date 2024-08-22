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

    @classmethod
    def from_dict(cls, src_dict: Dict[str, Any]):
        try:
            content = src_dict.get("content")
            role = src_dict.get("role")
            inner_working = src_dict.get("inner_working")
            return cls(content=content, role=role, inner_working=inner_working)
        except Exception as e:
            raise ValueError(f"Error creating Message from dict: {e}")

class ChatRequest(BaseModel):
    messages: list[Message]
    context: Optional[dict] = None
    model: Optional[str] = None
    options: Optional[dict] = None
    chain: Optional[str] = None

    def to_dict(self):
        dict = {}
        if self.model is not None:  
            dict['model'] = self.model
        dict['messages'] = [message.model_dump() for message in self.messages]
        return dict
    
    def get_last_question(self) -> str:
        for message in reversed(self.messages):
            if message.role == 'user':
                return message.content

        # Return an empty string if no user message is found
        return None
    
        



