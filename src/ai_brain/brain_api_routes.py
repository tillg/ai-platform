from typing import Any, Dict, Optional
import fastapi
from fastapi import Depends, FastAPI, Query, Request, Body, HTTPException
import logging
from ai_commons.apiModelsSearch import (
    Chunk,
    SearchRequest,
    SearchResultChunksAndDocuments,
    SearchResult,
)
from ai_brain.brain import Brain

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

router = fastapi.APIRouter()
brain = Brain.get_default_brain()


def _set_global_brain(brain_id: str):
    global brain
    logger.info(f"Setting global brain to {brain_id}")
    if not Brain.is_valid_brain_id(brain_id):
        raise HTTPException(
            status_code=400, detail=f"Brain with ID {brain_id} not found."
        )
    if brain_id != brain.parameters["id"]:
        logger.info(f"Instatiating brain {brain_id}")
        brain = Brain.get_brain_by_id(brain_id)


@router.get("/")
async def root():
    return {"message": "This is the AI Brain Service! 🧠"}


@router.get("/info")
async def info(brain_id: str) -> Dict[str, Any]:
    global brain
    _set_global_brain(brain_id)
    return brain.get_parameters_and_statistics()


@router.get("/list")
async def list():
    return Brain.get_brain_parameters_list()


@router.post("/search")
async def search(
    q: Optional[str] = None, body: Optional[SearchRequest] = Body(default=None)
) -> SearchResult:
    global brain
    logger.info(f"Search query: q={q}, body={body}")

    search_term = q or (body.search_term if body else None)
    logger.info(f"Search query: {search_term}")
    if not search_term:
        raise HTTPException(
            status_code=400,
            detail=(
                "A search term must be provided either as a query parameter or in the"
                " request body."
            ),
        )
    if body and body.brain_id:
        if not Brain.is_valid_brain_id(body.brain_id):
            raise HTTPException(
                status_code=400, detail=f"Brain with ID {body.brain_id} not found."
            )
        if body.brain_id != brain.get_parameters()["id"]:
            brain = Brain.get_brain_by_id(body.brain_id)
    search_result = brain.search_chunks_by_text(search_term)
    # search_result = SearchResultChunksAndDocuments(chunks=chunks)
    logger.info(f"Search result: {search_result}")
    return search_result
