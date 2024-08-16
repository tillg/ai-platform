from typing import Any, Dict
from ai_commons.apiModelsChat import ChatRequest, Message
import logging
from ai_orchestration.chain import Chain
from llm_wrapper_client.llm_client import Client as LlmClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Chain(Chain):
    
    def run(self, chat_request: ChatRequest, options: Dict[str, Any]) -> Message:
        logger.info(f"Running Simple_Rag chain with {chat_request} and options {options}")
        llm_client = LlmClient()
        message = llm_client.chat(chat_request)
        return message
    
    def get_name(self) -> str:
        return "naked_llm"
