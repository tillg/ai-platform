import fastapi
from ai_commons.api_models import Chunk
from ai_brain.brain import Brain
from ai_brain.brain_info_model import BrainInfo

router = fastapi.APIRouter()
brain = Brain()

@router.post("/search")
async def search(search_term: str) -> list[Chunk]:
    return brain.search_chunks_by_text(search_term)

@router.get("/info")
async def info() -> BrainInfo:
    return brain.get_brain_info()
