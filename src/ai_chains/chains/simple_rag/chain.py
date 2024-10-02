from typing import Any, Dict
from ai_commons.apiModelsChat import ChatRequest, Message
from ai_commons.apiModelsSearch import SearchRequest
import logging
from ai_chains.chain import Chain
from llm_wrapper_client.llm_client import Client as LlmClient
from prompt_lib.prompts import get_prompt
from ai_brain_client.ai_brain_client import Client as BrainClient
import copy
from ai_commons.inner_working import add_inner_working
import json
from pydantic import field_validator, validate_call

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Chain(Chain):
    
    def __init__(self, parameters: Dict[str, Any] = {}):
        super().__init__(parameters)
        logger.info(f"Creating Simple_Rag chain with parameters: {parameters}")
        
    @validate_call
    def run(self, chat_request: ChatRequest, parameters: Dict[str, Any] = {}) -> Message:
        logger.info(f"Running Simple_Rag chain with {chat_request} and parameters {json.dumps(parameters, indent=2)}")
        llm_client = LlmClient()
        brain_client = BrainClient()
        inner_working = {}

        # Get Document chunks
        question = chat_request.get_last_question()
        logger.info(f"{question=}")
        search_request = SearchRequest(search_term=question)
        search_result = brain_client.search_chunks_by_text(search_request)
        inner_working = add_inner_working(inner_working, "Step: Search Vector DB", search_result)

        documents = search_result.result.chunks_as_str()

        prompt_fields = {
            "documents": documents,
            "question": question
        }
        prompt = get_prompt("default_rag", **prompt_fields)

        chat_req_for_llm = copy.deepcopy(chat_request)
        chat_req_for_llm.messages[-1] = Message(content=prompt, role="user")

        answer = llm_client.chat(chat_req_for_llm)
        llm_iw = answer.inner_working
        llm_iw["prompt"] = prompt
        inner_working = add_inner_working(inner_working, "Step: Ask LLM", llm_iw)

        overall_answer = copy.deepcopy(answer)
        overall_answer.inner_working = inner_working

        return overall_answer
    
    def get_name(self) -> str:
        return "simple_rag"
