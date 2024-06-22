import unittest
import uuid
from ai_brain.brain import Brain
from ai_commons.api_models import Document, Chunk
import logging
from dotenv import load_dotenv
import os

load_dotenv()
logging.basicConfig(level=logging.INFO)

# in relation to this file my test data resides in ../../data/test_data
TEST_DATA_DIR = os.path.join(os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))), "data", "test_data")
TMP_DATA_DIR = os.path.join(TEST_DATA_DIR, "tmp")


class TestBrain(unittest.TestCase):

    def test_brain_initialization(self):
        brain = Brain(data_directory=TMP_DATA_DIR)

    def test_brain_add_doc(self):
        brain = Brain(data_directory=TMP_DATA_DIR)
        brain_size_pre = len(brain)
        doc = Document.from_text_file(os.path.join(
            TEST_DATA_DIR, "wikipedia_peru.txt"))
        brain.add_document(doc)
        brain_size_post = len(brain)
        self.assertEqual(brain_size_post-brain_size_pre, 1)


if __name__ == '__main__':
    unittest.main()
