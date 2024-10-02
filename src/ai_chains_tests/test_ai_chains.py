import unittest
import uuid
from ai_commons.apiModelsChat import ChatRequest, Message
from llm_wrapper.ollamaWrapper import get_models_as_json_array, get_models, get_default_model_name, chat
from ai_commons.apiModelsLlm import Model
from ai_chains.chain_factory import ChainFactory

class TestAiChains(unittest.TestCase):

    def test_ai_chain_factory_creation(self):
        factory = ChainFactory()
        self.assertIsNotNone(factory)

    def test_ai_chain_factory_chrreation_wo_existing_index(self):
        factory = ChainFactory(chains_index_file="a path that doesn't exist")
        self.assertIsNotNone(factory)