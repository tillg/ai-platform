from abc import ABC, abstractmethod
from typing import Any, Dict
from ai_commons.apiModelsChat import ChatRequest, Message

class Chain(ABC):
    def __init__(self, options: Dict[str, Any]):
        for key, value in options.items():
            setattr(self, key, value)
        
    @abstractmethod
    def run(self, chat_request: ChatRequest, options: dict = {}) -> Message:
        pass

    @abstractmethod
    def get_name(self) -> str:
        return "abstract"
