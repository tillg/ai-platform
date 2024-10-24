import unittest
import uuid
from ai_commons.apiModelsChat import ChatRequest, Message
from llm_wrapper.ollamaWrapper import (
    get_models_as_json_array,
    get_models,
    get_default_model_name,
    chat,
)
from ai_commons.apiModelsLlm import Model


class TestOllamaWrapper(unittest.TestCase):

    def test_model_list(self):
        models = get_models()
        self.assertIsNotNone(models)
        self.assertIsInstance(models, list, "Models should be a list")
        for model in models:
            self.assertIsInstance(
                model, Model, f"Each model should be a Model, but got '{type(model)}'"
            )

    def test_default_model(self):
        default_model_name = get_default_model_name()
        self.assertIsNotNone(default_model_name)
        self.assertIsInstance(default_model_name, str)

    def test_chat_with_pydantic_request(self):

        # Create sample Message instances
        message1 = Message(content="What is the capital of FRance?", role="user")
        message2 = Message(content="I'm fine, thank you!", role="assistant")  # noqa

        # Create a sample ChatRequest instance
        chat_request = ChatRequest(messages=[message1], model=get_default_model_name())

        chat_response = chat(chat_request)
        self.assertIsInstance(chat_response, Message)
        self.assertIsInstance(chat_response.content, str)


if __name__ == "__main__":
    unittest.main()
