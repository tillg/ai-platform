import unittest
import json
from ai_brain.chunker_char_text_splitter import ChunkerCharacterTextSplitter
from ai_commons.apiModelsSearch import Document, Chunk
import logging
from dotenv import load_dotenv
import os
from pydantic import ValidationError
from ai_brain.chunker_factory import ChunkerFactory

load_dotenv()
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# in relation to this file my test data resides in ../../data/test_data
TEST_DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "test_data"
)
TMP_DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "tmp"
)


class TestChunker(unittest.TestCase):

    def test_chunker_initialization(self):
        parameters = {
            "separator": "\n\n",
            "chunk_size": 256,
            "chunk_overlap": 20,
            "target_dir": TMP_DATA_DIR,
            "source_dir": TMP_DATA_DIR,
        }
        chunker = ChunkerCharacterTextSplitter(parameters)
        logger.info(f"{chunker=}")

    def test_chunker_initialization_with_defaults(self):
        parameters = {"target_dir": TMP_DATA_DIR, "source_dir": TMP_DATA_DIR}
        chunker = ChunkerCharacterTextSplitter(parameters)
        logger.info(f"{chunker=}")

    def test_chunker_fails_on_wrong_input(self):
        parameters = {
            "separator": "\n\n",
            "chunk_size": 256,
            "chunk_overlap": 20,
            "target_dir": TMP_DATA_DIR,
            "source_dir": TMP_DATA_DIR,
        }
        chunker = ChunkerCharacterTextSplitter(parameters)
        with self.assertRaises(ValidationError):
            chunker._chunkify_document("This is simply a string")

    def test_chunker_chunks(self):
        parameters = {
            "separator": "\n\n",
            "chunk_size": 256,
            "chunk_overlap": 20,
            "target_dir": TMP_DATA_DIR,
            "source_dir": TMP_DATA_DIR,
        }
        chunker = ChunkerCharacterTextSplitter(parameters)
        doc = Document.from_text_file(os.path.join(TEST_DATA_DIR, "wikipedia_peru.txt"))
        chunks = chunker._chunkify_document(doc)
        for chunk in chunks:
            self.assertIsInstance(chunk, Chunk)

    def test_chunker_chunks_with_other_settings(self):
        parameters = {
            "separator": "\n",
            "chunk_size": 1000,
            "chunk_overlap": 100,
            "target_dir": TMP_DATA_DIR,
            "source_dir": TMP_DATA_DIR,
        }
        chunker = ChunkerCharacterTextSplitter(parameters)
        doc = Document.from_text_file(os.path.join(TEST_DATA_DIR, "wikipedia_peru.txt"))
        chunks = chunker._chunkify_document(doc)
        for chunk in chunks:
            self.assertIsInstance(chunk, Chunk)

    def test_chunker_initialization_with_defaults_and_params_returned(self):
        parameters = {"target_dir": TMP_DATA_DIR, "source_dir": TMP_DATA_DIR}
        chunker = ChunkerCharacterTextSplitter(parameters)
        params = chunker.get_parameters()
        # formatted_params = json.dumps(params, indent=4)
        # logger.info(f"Params: {formatted_params}")
        self.assertIn("separator", params)

    def test_chunker_factory(self):
        factory = ChunkerFactory()
        parameters = {
            "chunker_type": "character_text_splitter",
            "target_dir": TMP_DATA_DIR,
            "source_dir": TMP_DATA_DIR,
        }
        chunker = factory.create_chunker(parameters)
        parameters = chunker.get_parameters()
        formatted_params = json.dumps(parameters, indent=4)
        logger.info(f"Params from chunmker created by factory: {
                    formatted_params}")
        self.assertIsInstance(chunker, ChunkerCharacterTextSplitter)

    def test_chunker_factory_with_default(self):
        factory = ChunkerFactory()
        parameters = {"target_dir": TMP_DATA_DIR, "source_dir": TMP_DATA_DIR}
        chunker = factory.create_chunker(parameters)
        params = chunker.get_parameters()
        formatted_params = json.dumps(params, indent=4)
        logger.info(f"Params from chunmker created by factory without any params: {
                    formatted_params}")
        self.assertIsInstance(chunker, ChunkerCharacterTextSplitter)

    def test_chunker_do_chunkify(self):
        factory = ChunkerFactory()
        parameters = {
            "target_dir": os.path.join(TMP_DATA_DIR, "chunked_documents"),
            "source_dir": os.path.join(TEST_DATA_DIR, "documents_to_chunk"),
        }
        chunker = factory.create_chunker(parameters)
        params = chunker.get_parameters()
        formatted_params = json.dumps(params, indent=4)
        logger.info(f"Params from chunmker created by factory for do_chunkify test: {
                    formatted_params}")
        chunker.do_chunkify()


if __name__ == "__main__":
    unittest.main()
