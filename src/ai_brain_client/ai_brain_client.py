import ssl
from typing import Any, Dict, List, Optional, Union

import httpx
from attrs import define, evolve, field
from ai_commons.apiModelsChat import ChatRequest, Message
from ai_commons.apiModelsLlm import Model
import logging
from ai_commons.constants import AI_BRAIN_HOST, AI_BRAIN_PORT
from ai_commons.apiModelsSearch import BrainModel, SearchResult, SearchRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 60s timeout for reading (i.e. getting the first package of an answer), and a 5s timeout elsewhere.
TIMEOUT = httpx.Timeout(5.0, read=60.0)

@define
class Client:
    """A class for easily accessing a ai_brain service.
    """

    raise_on_unexpected_status: bool = field(default=False, kw_only=True)
    _base_url: str = field(alias="base_url", default=f"http://{
                           AI_BRAIN_HOST}:{AI_BRAIN_PORT}")
    _timeout: Optional[httpx.Timeout] = field(
        default=TIMEOUT, kw_only=True, alias="timeout")
    _client: Optional[httpx.Client] = field(default=None, init=False)
    _async_client: Optional[httpx.AsyncClient] = field(
        default=None, init=False)
    
    def get_httpx_client(self) -> httpx.Client:
        """Get the underlying httpx.Client, constructing a new one if not previously set"""
        logger.info(f"Client get_httpx_client: {self._client}")
        if self._client is None:
            self._client = httpx.Client(
                base_url=self._base_url,
                timeout=self._timeout,
            )
        logger.info(f"LLM Client get_httpx_client: {self._client}")
        return self._client

    def get_brain_list(self) -> List[BrainModel]:
        response = self.get_httpx_client().get("/list")
        logger.info(f"GET /list: {response}")
        response.raise_for_status()
        return [BrainModel(**x) for x in response.json()]
    
    def search_chunks_by_text(self,  search_request: SearchRequest) -> SearchResult:
        response = self.get_httpx_client().post("/search", json=search_request.model_dump())
        logger.info(f"POST /search: {response}")
        response.raise_for_status()
        return SearchResult(**response.json())