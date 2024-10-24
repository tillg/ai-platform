from fastapi import Depends, FastAPI
import uvicorn
from ai_commons.constants import AI_CHAINS_HOST, AI_CHAINS_PORT
import ai_chains.chain_api_routes
import logging
import ai_commons.constants as constants
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

logger.info(f"Orchestration port: {AI_CHAINS_PORT}")

app = FastAPI(
    title="AI Chains",
    description="Interact with AI chains that combine vector databases and LLMs.",
)
allowed_origins = ["*"]
# Add CORSMiddleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(ai_chains.chain_api_routes.router)


def start_ai_chains(reload=False):
    uvicorn.run(
        "ai_chains.main:app", host=AI_CHAINS_HOST, port=AI_CHAINS_PORT, reload=reload
    )


def main():
    start_ai_chains(reload=True)


if __name__ == "__main__":
    main()
