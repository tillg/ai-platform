import ssl
from typing import Any, Dict, List, Optional, Union

import httpx
from attrs import define, evolve, field
from ai_commons.apiModelsChat import ChatRequest, Message
from ai_commons.apiModelsLlm import Model
import logging
from ai_commons.constants import AI_LLM_WRAPPER_HOST, AI_LLM_WRAPPER_PORT

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

# 60s timeout for reading (i.e. getting the first package of an answer), and a 5s
# timeout elsewhere.
TIMEOUT = httpx.Timeout(5.0, read=60.0)


@define
class Client:
    """A class for easily accessing a llm_wrapper service."""

    raise_on_unexpected_status: bool = field(default=False, kw_only=True)
    _base_url: str = field(alias="base_url", default=f"http://{
                           AI_LLM_WRAPPER_HOST}:{AI_LLM_WRAPPER_PORT}")
    _timeout: Optional[httpx.Timeout] = field(
        default=TIMEOUT, kw_only=True, alias="timeout"
    )
    _client: Optional[httpx.Client] = field(default=None, init=False)
    _async_client: Optional[httpx.AsyncClient] = field(default=None, init=False)

    def get_httpx_client(self) -> httpx.Client:
        """Get the underlying httpx.Client, constructing a new one if
        not previously set"""
        logger.info(f"Client get_httpx_client: {self._client}")
        if self._client is None:
            self._client = httpx.Client(
                base_url=self._base_url,
                timeout=self._timeout,
            )
        logger.info(f"LLM Client get_httpx_client: {self._client}")
        return self._client

    def get_async_httpx_client(self) -> httpx.AsyncClient:
        """Get the underlying httpx.AsyncClient, constructing a new one if not
        previously set"""
        if self._async_client is None:
            self._async_client = httpx.AsyncClient(
                base_url=self._base_url,
                headers=self._headers,
                timeout=self._timeout,
                verify=self._verify_ssl,
                follow_redirects=self._follow_redirects,
                **self._httpx_args,
            )
        return self._async_client

    def get_models(self) -> List[Model]:
        response = self.get_httpx_client().get("/models")
        logger.info(f"GET /models: {response}")
        response.raise_for_status()
        return [Model(**x) for x in response.json()]

    def chat(self, chat_request: ChatRequest) -> Message:
        response = self.get_httpx_client().post("/chat", json=chat_request.dict())
        logger.info(f"POST /chat: {response}")
        response.raise_for_status()
        return Message(**response.json())
