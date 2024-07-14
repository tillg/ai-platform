from fastapi import Depends, FastAPI, Query
import uvicorn

import logging
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
import llm_wrapper.api_routes
from ai_commons.constants import AI_LLM_WRAPPER_PORT

load_dotenv()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


logger.info(f"LLM Wrapper port: {AI_LLM_WRAPPER_PORT}")

app = FastAPI()
allowed_origins = ["*"]
# Add CORSMiddleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(llm_wrapper.api_routes.router)


if __name__ == "__main__":
    uvicorn.run("llm_wrapper.main:app",
                host="0.0.0.0", port=AI_LLM_WRAPPER_PORT, reload=True)
