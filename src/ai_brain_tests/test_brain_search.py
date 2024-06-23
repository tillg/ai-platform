import unittest
import uuid
from ai_brain.brain import Brain
from ai_commons.api_models import Document, Chunk
from utils.utils import get_now_as_string
import logging
from dotenv import load_dotenv
import os
import string
import random

load_dotenv()
logging.basicConfig(level=logging.INFO)

# in relation to this file my test data resides in ../../data/test_data
TEST_DATA_DIR = os.path.join(os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))), "data", "test_data")
TMP_DATA_DIR = os.path.join(TEST_DATA_DIR, "tmp")

LONG_ARTICLE = "wikipedia_peru.txt"
SHORT_ARTICLE = "rectus_abdominus.txt"




class TestBrainSearch(unittest.TestCase):

    def test_brain_search1(self):
        brain = Brain(data_directory=TMP_DATA_DIR)
        brain.delete_all()
        brain_size_pre = len(brain)
        doc1 = Document.from_text_file(os.path.join(
            TEST_DATA_DIR, LONG_ARTICLE))
        doc2 = Document.from_text_file(os.path.join(
            TEST_DATA_DIR, SHORT_ARTICLE))
        brain.add_documents([doc1, doc2])
        brain_size_post = len(brain)
        self.assertEqual(brain_size_post-brain_size_pre, 2)
        chunks = brain.search_chunks_by_text("Peru politics")
        self.assertEqual(len(chunks), 10)
        self.assertIsInstance(chunks, list, "Expected 'chunks' to be a list")

        # Assert that all items in `chunks` are instances of Chunk
        for chunk in chunks:
            self.assertIsInstance(
                chunk, Chunk, "Expected item to be an instance of Chunk")
        
        # For inspection write the chunks in a file
        dir = os.path.join(TMP_DATA_DIR, get_now_as_string())
        for chunk in chunks:
            chunk.write_2_file(dir)
            
if __name__ == '__main__':
    unittest.main()
