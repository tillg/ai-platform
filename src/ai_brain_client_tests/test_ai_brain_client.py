import unittest
from ai_commons.apiModelsChat import ChatRequest, Message
from ai_brain_client.ai_brain_client import Client as AiBrainClient
from ai_commons.apiModelsLlm import Model
from ai_commons.apiModelsSearch import Document, Chunk, SearchResultChunksAndDocuments, SearchResult, BrainModel, SearchRequest
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class TestAiBrainClient(unittest.TestCase):
    
    def test_brain_list(self):
        ai_brain_client = AiBrainClient()
        brains = ai_brain_client.get_brain_list()
        
        self.assertIsNotNone(brains)
        self.assertIsInstance(brains, list, "Brains should be a list")
        logger.info(f"Brains: {brains}")
        for brain in brains:
            self.assertIsInstance(
                brain, BrainModel, f"Each model should be a Model, but got '{type(brain)}'")

    def test_search_chunks_by_text(self):
        ai_brain_client = AiBrainClient()

        search_request = SearchRequest(search_term="what can i do in Berlin?")
        search_result = ai_brain_client.search_chunks_by_text(search_request)

        self.assertIsInstance(search_result, SearchResult)
        self.assertIsNotNone(search_result.result.chunks)

        logger.info(f"Search result: {search_result}")

if __name__ == '__main__':
    unittest.main()
