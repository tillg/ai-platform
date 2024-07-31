from typing import Any, Dict, List, Optional
import uuid
from pydantic import BaseModel
from langchain.docstore.document import Document as lc_Document
import os
from utils.dict2file import write_dict_to_file, read_dict_from_file


class Model(BaseModel):
    name: str
    description: Optional[str] = None
    details: Optional[Dict[str, str]] = None
    state: Optional[str]
