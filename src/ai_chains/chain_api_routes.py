from typing import List
import fastapi
from ai_commons.apiModelsChat import ChatRequest, Message#
import logging
from ai_chains.chain_factory import ChainFactory

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

router = fastapi.APIRouter()
chain_factory = ChainFactory()
chain = chain_factory.create_chain({})

def _set_global_chain(chain_id: str):
    global chain
    logger.info(f"Setting global chain to {chain_id}")
    if not chain_factory.is_valid_chain_id(chain_id):
        raise fastapi.HTTPException(
            status_code=400, detail=f"Chain with ID {chain_id} not found.")
    current_chain_id = chain.parameters.get("id", None)
    if chain_id != current_chain_id:
        logger.info(f"Instatiating chain {chain_id}")
        chain = chain_factory.create_chain_by_id(chain_id)

@router.get("/")
async def root():
    return {"message": "This is the AI Orchestration Service!"}

@router.get("/list", 
            response_model=List[str],
            summary="get the list of available chains",
            )
async def list_chains():
    chains = chain_factory.get_chain_list()
    return chains

@router.post("/run_chain")
async def run_chain(chat_request: ChatRequest) -> Message:
    logger.info(f"Running Chain with {chat_request}")
    _set_global_chain(chat_request.chain)
    response = chain.run(chat_request)
    response.inner_working["chain"] = chain.get_name()
    return response
