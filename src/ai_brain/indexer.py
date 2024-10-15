from ai_commons.apiModelsSearch import Document, Chunk
from typing import Any, Dict, List
import logging
import os
from pydantic import validate_call

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class Indexer:

    @validate_call
    def __init__(self, parameters: Dict[str, Any]):
        self.parameters = parameters
        # Check that we have a source_dir
        if "source_dir" not in parameters:
            raise ValueError("source_dir is required for Indexer.")
