import unittest
from ai_commons.apiModelsChat import ChatRequest, Message
from llm_wrapper_client.llm_client import Client
from ai_commons.apiModelsLlm import Model
from utils_tests.base_fastapi_test import BaseTest
from ai_commons.constants import AI_LLM_WRAPPER_PORT


class TestLlmWrapperClient(BaseTest):
    server_port = AI_LLM_WRAPPER_PORT
    server_app = "llm_wrapper.main:app"

    def test_model_list(self):
        client = Client()
        models = client.get_models()

        self.assertIsNotNone(models)
        self.assertIsInstance(models, list, "Models should be a list")
        for model in models:
            self.assertIsInstance(
                model, Model, f"Each model should be a Model, but got '{type(model)}'"
            )

    # def test_default_model(self):
    #     default_model = get_default_model()
    #     self.assertIsNotNone(default_model)
    #     self.assertIsInstance(default_model, Model)

    def test_chat_with_pydantic_request(self):
        client = Client()

        # Create sample Message instances
        message1 = Message(content="What is the capital of FRance?", role="user")
        message2 = Message(content="I'm fine, thank you!", role="assistant")  # noqa

        # Create a sample ChatRequest instance
        chat_request = ChatRequest(
            messages=[message1],
        )

        chat_response = client.chat(chat_request)
        self.assertIsInstance(chat_response, Message)
        self.assertIsInstance(chat_response.content, str)


if __name__ == "__main__":
    unittest.main()
