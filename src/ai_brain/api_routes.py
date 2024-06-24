import fastapi
from ai_commons.api_models import Chunk, SearchRequest, SearchResult
from ai_brain.brain import Brain
from ai_brain.brain_info_model import BrainInfo


router = fastapi.APIRouter()
brain = Brain()


@router.post("/search")
async def search(request: SearchRequest) -> SearchResult:
    chunks =  brain.search_chunks_by_text(request.search_term)
    search_result = SearchResult(chunks=chunks)
    return search_result


@router.get("/info")
async def info() -> BrainInfo:
    return brain.get_brain_info()
