from typing import Any, Dict, Optional
import fastapi
from fastapi import Depends, FastAPI, Query, Request, Body, HTTPException
import logging
from ai_commons.api_models import Chunk, SearchRequest, SearchResultChunksAndDocuments, SearchResult
from ai_brain.brain import Brain
from ai_brain_loaders.ai_brain_loader_wikipedia import load_page_tree_to_brain

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = fastapi.APIRouter()
brain = Brain()


@router.get("/")
async def root():
    return {"message": "This is the AI Brain Service! 🧠"}


@router.get("/info")
async def info() -> Dict[str, Any]:
    return brain.get_brain_info()


@router.get("/load")
def load():
    load_page_tree_to_brain(brain)
    return (brain.get_brain_info())


@router.get("/delete_all")
def delete_all():
    brain.delete_all()
    return brain.get_brain_info()


@router.post("/search")
async def search(request: Request, q: Optional[str] = None, body: Optional[SearchRequest] = Body(default=None)) -> SearchResult:
    logger.info(f"Search query: q={q}, body={body}")

    search_term = q or (body.search_term if body else None)
    logger.info(f"Search query: {search_term}")
    if not search_term:
        raise HTTPException(
            status_code=400, detail="A search term must be provided either as a query parameter or in the request body.")
    search_result = brain.search_chunks_by_text(search_term)
    #search_result = SearchResultChunksAndDocuments(chunks=chunks)
    logger.info(f"Search result: {search_result}")
    return search_result
