from fastapi import Depends, FastAPI, Query
import uvicorn

import logging
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
import llm_wrapper.llm_api_routes
from ai_commons.constants import AI_LLM_WRAPPER_HOST, AI_LLM_WRAPPER_PORT

load_dotenv()
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


logger.info(f"LLM Wrapper port: {AI_LLM_WRAPPER_PORT}")

app = FastAPI(
    title="LLM Wrapper",
    description="A uniform wrapper for multiple LLM models.",
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

app.include_router(llm_wrapper.llm_api_routes.router)


def start_llm_wrapper(reload=False):
    uvicorn.run(
        "llm_wrapper.main:app",
        host=AI_LLM_WRAPPER_HOST,
        port=AI_LLM_WRAPPER_PORT,
        reload=reload,
    )


if __name__ == "__main__":
    start_llm_wrapper(reload=True)
