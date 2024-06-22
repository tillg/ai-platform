import unittest
import uuid
from ai_brain.chunker import Chunker
from ai_commons.api_models import Document, Chunk
import logging
from dotenv import load_dotenv
import os
from pydantic import ValidationError

load_dotenv()
logging.basicConfig(level=logging.INFO)

# in relation to this file my test data resides in ../../data/test_data
TEST_DATA_DIR = os.path.join(os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))), "data", "test_data")


class TestChunker(unittest.TestCase):

    def test_chunker_initialization(self):
        chunker = Chunker(separator="\n\n", chunk_size=256, chunk_overlap=20)

    def test_chunker_initialization_with_defaults(self):
        chunker = Chunker()

    def test_chunker_fails_on_wrong_input(self):
        chunker = Chunker(separator="\n\n", chunk_size=256, chunk_overlap=20)
        with self.assertRaises(ValidationError):
            chunker.chunkify("This is simply a string")

    def test_chunker_chunks(self):
        chunker = Chunker(separator="\n\n", chunk_size=256, chunk_overlap=20)
        doc = Document.from_text_file(os.path.join(
            TEST_DATA_DIR, "wikipedia_peru.txt"))
        chunks = chunker.chunkify(doc)
        for chunk in chunks:
            self.assertIsInstance(chunk, Chunk)

    def test_chunker_chunks_with_other_settings(self):
        chunker = Chunker(separator="\n", chunk_size=1000, chunk_overlap=100)
        doc = Document.from_text_file(os.path.join(
            TEST_DATA_DIR, "wikipedia_peru.txt"))
        chunks = chunker.chunkify(doc)
        for chunk in chunks:
                self.assertIsInstance(chunk, Chunk)

if __name__ == '__main__':
    unittest.main()

