from typing import Any, Dict
from ai_commons.apiModelsChat import ChatRequest, Message
import logging
from ai_chains.chain import Chain

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
<<<<<<< HEAD
=======

>>>>>>> gitbutler/integration

class Chain(Chain):
    def run(self, chat_request: ChatRequest, options: Dict[str, Any]) -> Message:
        logger.info(f"Running Default chain with {chat_request} and options {options}")
        message = Message(
            content="Hello World",
            role="assistant",
            inner_working={"status": "All easy 😉"},
        )
        return message

    def get_name(self) -> str:
        return "default"
