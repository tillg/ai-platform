import unittest
import json
from ai_brain.chunker_char_text_splitter import ChunkerCharacterTextSplitter
from ai_commons.api_models import Document, Chunk
import logging
from dotenv import load_dotenv
import os
from pydantic import ValidationError
from ai_brain.chunker_factory import ChunkerFactory

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# in relation to this file my test data resides in ../../data/test_data
TEST_DATA_DIR = os.path.join(os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))), "data", "test_data")


class TestChunker(unittest.TestCase):

    def test_chunker_initialization(self):
        chunker = ChunkerCharacterTextSplitter(
            {"separator": "\n\n", "chunk_size": 256, "chunk_overlap": 20})

    def test_chunker_initialization_with_defaults(self):
        chunker = ChunkerCharacterTextSplitter({})

    def test_chunker_fails_on_wrong_input(self):
        chunker = ChunkerCharacterTextSplitter(
            {"separator": "\n\n", "chunk_size": 256, "chunk_overlap": 20})
        with self.assertRaises(ValidationError):
            chunker.chunkify("This is simply a string")

    def test_chunker_chunks(self):
        chunker = ChunkerCharacterTextSplitter(
            {"separator": "\n\n", "chunk_size": 256, "chunk_overlap": 20})
        doc = Document.from_text_file(os.path.join(
            TEST_DATA_DIR, "wikipedia_peru.txt"))
        chunks = chunker.chunkify(doc)
        for chunk in chunks:
            self.assertIsInstance(chunk, Chunk)

    def test_chunker_chunks_with_other_settings(self):
        chunker = ChunkerCharacterTextSplitter(
            {"separator": "\n", "chunk_size": 1000, "chunk_overlap": 100})
        doc = Document.from_text_file(os.path.join(
            TEST_DATA_DIR, "wikipedia_peru.txt"))
        chunks = chunker.chunkify(doc)
        for chunk in chunks:
            self.assertIsInstance(chunk, Chunk)

    def test_chunker_initialization_with_defaults_and_params_returned(self):
        chunker = ChunkerCharacterTextSplitter({})
        params = chunker.get_params()
        # formatted_params = json.dumps(params, indent=4)
        # logger.info(f"Params: {formatted_params}")        
        self.assertIn("separator", params)

    def test_chunker_factory(self):
        factory = ChunkerFactory()
        chunker = factory.create_chunker(
            {"chunker_type": "ChunkerCharacterTextSplitter"})
        params = chunker.get_params()
        formatted_params = json.dumps(params, indent=4)
        logger.info(f"Params from chunmker created by factory: {formatted_params}")
        self.assertIsInstance(chunker, ChunkerCharacterTextSplitter)

    def test_chunker_factory_with_default(self):
        factory = ChunkerFactory()
        chunker = factory.create_chunker(
            {})
        params = chunker.get_params()
        formatted_params = json.dumps(params, indent=4)
        logger.info(f"Params from chunmker created by factory without any params: {
                    formatted_params}")
        self.assertIsInstance(chunker, ChunkerCharacterTextSplitter)

if __name__ == '__main__':
    unittest.main()
