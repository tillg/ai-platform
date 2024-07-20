import unittest
import uuid
from ai_brain.brain import Brain
from ai_commons.api_models import Document, Chunk
import logging
from dotenv import load_dotenv
import os, string, random

load_dotenv()
logging.basicConfig(level=logging.INFO)

# in relation to this file my test data resides in ../../data/test_data
TEST_DATA_DIR = os.path.join(os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))), "data", "test_data")
TMP_DATA_DIR = os.path.join(os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))), "data", "tmp")

LONG_ARTICLE = "wikipedia_peru.txt"
SHORT_ARTICLE = "rectus_abdominus.txt"


class TestBrainManager(unittest.TestCase):

    def test_get_brain_list(self):
        brains_list = Brain.get_brain_list(brains_directory=TEST_DATA_DIR)
        logging.info(brains_list)
        self.assertTrue(len(brains_list) == 1)

if __name__ == '__main__':
    unittest.main()
