import unittest
import uuid
from ai_brain.brain import Brain
from ai_commons.apiModelsSearch import Document, Chunk
from utils.utils import get_now_as_string
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

class TestBrainSearch(unittest.TestCase):

    def prep_chunk_directory(self):
        path_to_docs = os.path.join(TMP_DATA_DIR, get_now_as_string()+"_docs")
        path_to_chunks = os.path.join(TMP_DATA_DIR, get_now_as_string()+"_chunks")
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
        brain = Brain({"data_directory": TMP_DATA_DIR,
                       "path": get_now_as_string()+'_test_brain_search1',
                       })

        brain_size_pre = len(brain)
        doc1 = Document.from_text_file(os.path.join(
            TEST_DATA_DIR, LONG_ARTICLE))
        doc2 = Document.from_text_file(os.path.join(
            TEST_DATA_DIR, SHORT_ARTICLE))
        chunks = Chunk.from_json_directory(chunk_dir) 
        brain.import_documents([doc1, doc2])
        brain.import_chunks(chunks)

        brain_size_post = len(brain)
        self.assertEqual(brain_size_post-brain_size_pre, 2)
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
