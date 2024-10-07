from abc import ABC, abstractmethod
from typing import Any, Dict
from ai_commons.apiModelsChat import ChatRequest, Message
from pydantic import validate_call
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Chain(ABC):
    def __init__(self, parameters: Dict[str, Any]):
        logger.info(f"Creating chain with parameters: {parameters}")
        self.parameters = parameters
        
    @abstractmethod
    @validate_call
    def run(self, chat_request: ChatRequest, parameters: Dict[str, Any] = {}) -> Message:
        pass

    @abstractmethod
    def get_name(self) -> str:
        return "abstract"
