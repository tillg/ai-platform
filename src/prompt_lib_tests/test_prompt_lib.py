import unittest
from prompt_lib.prompts import get_prompt_template, get_prompt
import logging


# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
handler = logging.StreamHandler()
handler.setLevel(logging.WARNING)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class TestPromptLib(unittest.TestCase):
    
    def test_get_prompt_template(self):

        prompt_template = get_prompt_template("default")

        self.assertIsNotNone(prompt_template)
        self.assertIsInstance(prompt_template, str, "Prompt Templates should be a string")
  
    def test_get_prompt(self):
        prompt_fields = {
         "documents": """
Marie Curie (1867-1934) was a Polish and naturalised-French physicist and chemist who conducted pioneering research on radioactivity. Born in Warsaw, she studied in Poland until she was 24, when she moved to Paris to earn her higher degrees.
  """,
         "question": "Was Marie-Curie french?"
     }
        prompt = get_prompt("default_rag", **prompt_fields)
        logger.info(f"Prompt: {prompt}")
        self.assertIsNotNone(prompt)
        self.assertIsInstance(prompt, str, "Prompt should be a string")

if __name__ == '__main__':
    unittest.main()
