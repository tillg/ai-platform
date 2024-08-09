from typing import List
from utils.sub_modules import list_submodules
import ai_orchestration.chains
from ai_commons.apiModelsChat import ChatRequest, Message

CHAIN_LIST = ["deafult", "simple_rag"]

def get_chains() -> List[str]:
    return CHAIN_LIST

def run_chain(chat_request: ChatRequest, chain_name: str) -> Message:
    chain = get_chain(chain_name, chat_request.options)
    chain_result = chain.run(chat_request, chat_request.options)
    return chain_result


def get_chain(chain_name: str, options ):
    if chain_name == "simple_rag_chain":
        from ai_orchestration.chains.simple_rag_chain.chain import Chain
        return Chain(options=options)
    else:
        from ai_orchestration.chains.default.chain import Chain
        return Chain(options=options)
    
