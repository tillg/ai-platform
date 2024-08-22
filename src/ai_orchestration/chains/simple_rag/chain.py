from typing import Any, Dict
from ai_commons.apiModelsChat import ChatRequest, Message
from ai_commons.apiModelsSearch import SearchRequest
import logging
from ai_orchestration.chain import Chain
from llm_wrapper_client.llm_client import Client as LlmClient
from prompt_lib.prompts import get_prompt
from ai_brain_client.ai_brain_client import Client as BrainClient
import copy

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Chain(Chain):
    
    def run(self, chat_request: ChatRequest, options: Dict[str, Any]) -> Message:
        logger.info(f"Running Simple_Rag chain with {chat_request} and options {options}")
        llm_client = LlmClient()
        brain_client = BrainClient()

        # Get Document chunks
        question = chat_request.get_last_question()
        inner_working = {}
        inner_working["search_str"] = question
        logger.info(f"{question=}")
        search_request = SearchRequest(search_term=question)
        search_result = brain_client.search_chunks_by_text(search_request)
        inner_working.update(search_result.inner_working)

        documents = search_result.result.chunks_as_str()

        prompt_fields = {
            "documents": documents,
            "question": question
        }
        prompt = get_prompt("default_rag", **prompt_fields)

        chat_req_for_llm = copy.deepcopy(chat_request)
        chat_req_for_llm.messages[-1] = Message(content=prompt, role="user")

        answer = llm_client.chat(chat_req_for_llm)
        return answer
    
    def get_name(self) -> str:
        return "naked_llm"
