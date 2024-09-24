import unittest
import uuid
from ai_brain.brain import Brain
from ai_commons.apiModelsSearch import BrainParameters, Document, Chunk
from utils.utils import get_now_as_string, simplify_text
import logging
import os
import string
import random
from ai_commons.constants import TEST_DATA_DIR, TMP_DATA_DIR
from ai_brain.chunker_factory import ChunkerFactory
import shutil

logging.basicConfig(level=logging.INFO)

LONG_ARTICLE = "wikipedia_peru.txt"
SHORT_ARTICLE = "rectus_abdominus.txt"


# Configure logging
logging.basicConfig(level=logging.INFO)

class TestBrainSearch(unittest.TestCase):

    def prep_chunk_directory(self):
        path_to_docs = os.path.join(TMP_DATA_DIR, simplify_text(get_now_as_string()+"_docs"))
        path_to_chunks = os.path.join(
            TMP_DATA_DIR, simplify_text(get_now_as_string()+"_chunks"))
        shutil.rmtree(path_to_chunks, ignore_errors=True)
        doc1 = Document.from_text_file(os.path.join(
            TEST_DATA_DIR, LONG_ARTICLE))
        doc2 = Document.from_text_file(os.path.join(
            TEST_DATA_DIR, SHORT_ARTICLE))
        doc1.write_2_json(path_to_docs)
        doc2.write_2_json(path_to_docs)
        parameters = {"source_dir": path_to_docs, "target_dir": path_to_chunks}
        chunker = ChunkerFactory().create_chunker(parameters)
        chunker.do_chunkify()
        return path_to_chunks

    def test_brain_search1(self):
        chunk_dir = self.prep_chunk_directory()
        brain_parameters = BrainParameters(id="whatever",
                                           name="whatever",
                                           description="whatever",
                                           data_directory=os.path.join(
                                               TMP_DATA_DIR, get_now_as_string()+"test_brain_search1"),
                                           scraper=None,
                                           allow_duplicates=True,
                                           chunks_directory= chunk_dir)
        brain = Brain(brain_parameters)

        brain_size_pre = brain.number_of_documents()
        doc1 = Document.from_text_file(os.path.join(
            TEST_DATA_DIR, LONG_ARTICLE))
        doc2 = Document.from_text_file(os.path.join(
            TEST_DATA_DIR, SHORT_ARTICLE))
        chunks = Chunk.from_json_directory(chunk_dir)
        brain.import_documents([doc1, doc2])
        brain.import_chunks_from_directory()

        brain_size_post = brain.number_of_documents()
        self.assertEqual(brain_size_post-brain_size_pre, 2 , "Expected brain size to be 2 documents")
        chunks = brain.search_chunks_by_text("Peru politics").result.chunks
        self.assertEqual(len(chunks), 10)
        self.assertIsInstance(chunks, list, "Expected 'chunks' to be a list")

        # Assert that all items in `chunks` are instances of Chunk
        for chunk in chunks:
            self.assertIsInstance(
                chunk, Chunk, "Expected item to be an instance of Chunk")

        # For inspection write the chunks in a file
        dir = os.path.join(TMP_DATA_DIR, get_now_as_string())
        for chunk in chunks:
            chunk.write_2_json(dir)


if __name__ == '__main__':
    unittest.main()
