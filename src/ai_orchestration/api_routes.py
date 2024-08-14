from typing import List
import fastapi
from ai_commons.apiModelsChat import ChatRequest, Message#
import logging
from ai_orchestration.ai_orchestrator import get_chains, run_chain, get_chain_by_name

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = fastapi.APIRouter()

@router.get("/")
async def root():
    return {"message": "This is the AI Orchestration Service!"}


@router.get("/list", 
            response_model=List[str],
            summary="get the list of available chains",
            )
async def list_chains():
    chains = get_chains()
    return chains

@router.post("/run_chain")
async def chain(chat_request: ChatRequest) -> Message:
    logger.info(f"Running Chain with {chat_request}")
    chain = get_chain_by_name(chat_request.chain, chat_request.options)
    response = chain.run(chat_request, chain)
    response.inner_working["chain"] = chain.get_name()
    return response
