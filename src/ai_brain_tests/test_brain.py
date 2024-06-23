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
TMP_DATA_DIR = os.path.join(TEST_DATA_DIR, "tmp")

LONG_ARTICLE = "wikipedia_peru.txt"
SHORT_ARTICLE = "rectus_abdominus.txt"

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

class TestBrain(unittest.TestCase):

    def test_brain_initialization(self):
        brain = Brain(data_directory=TMP_DATA_DIR)

    def test_brain_add_doc(self):
        brain = Brain(data_directory=TMP_DATA_DIR)
        brain_size_pre = len(brain)
        doc = Document.from_text_file(os.path.join(
            TEST_DATA_DIR, LONG_ARTICLE))
        brain.add_document(doc)
        brain_size_post = len(brain)
        self.assertEqual(brain_size_post-brain_size_pre, 1)

    def test_brain_add_multiple_docs(self):
        brain = Brain(data_directory=TMP_DATA_DIR)
        brain_size_pre = len(brain)
        doc1 = Document.from_text_file(os.path.join(
            TEST_DATA_DIR, LONG_ARTICLE))
        doc2 = Document.from_text_file(os.path.join(
            TEST_DATA_DIR, SHORT_ARTICLE))
        brain.add_documents([doc1, doc2])
        brain_size_post = len(brain)
        self.assertEqual(brain_size_post-brain_size_pre, 2)

    def test_brain_get_doc_by_id(self):
        brain = Brain(data_directory=TMP_DATA_DIR)
        doc = Document.from_text_file(os.path.join(
            TEST_DATA_DIR, SHORT_ARTICLE))
        brain.add_document(doc)
        doc_id = doc.id
        doc_retrieved = brain.get_document_by_id(doc_id)
        self.assertEqual(doc, doc_retrieved)

    def test_brain_get_doc_by_uri(self):
        brain = Brain(data_directory=TMP_DATA_DIR)
        doc = Document.from_text_file(os.path.join(
            TEST_DATA_DIR, SHORT_ARTICLE))
        doc.uri = generate_random_string(10)
        brain.add_document(doc)
        doc_retrieved = brain.get_document_by_uri(doc.uri)
        self.assertEqual(doc, doc_retrieved)

    def test_brain_delete_all(self):
        brain = Brain(data_directory=TMP_DATA_DIR)
        doc = Document.from_text_file(os.path.join(
            TEST_DATA_DIR, SHORT_ARTICLE))
        brain.add_document(doc)
        brain.delete_all()
        self.assertEqual(len(brain), 0)

    def test_brain_delete_all_and_then_add_a_doc(self):
        brain = Brain(data_directory=TMP_DATA_DIR)
        doc = Document.from_text_file(os.path.join(
            TEST_DATA_DIR, SHORT_ARTICLE))
        brain.add_document(doc)
        brain.delete_all()
        self.assertEqual(len(brain), 0)
        brain.add_document(doc)
        self.assertEqual(len(brain), 1)

    def test_add_doc_without_duplicate(self):
        brain = Brain(data_directory=TMP_DATA_DIR)
        pre_size = len(brain)
        doc = Document.from_text_file(os.path.join(
            TEST_DATA_DIR, SHORT_ARTICLE))
        brain.add_document(doc)
        brain.add_document(doc,allow_duplicates=False)
        brain_increase = len(brain) - pre_size
        self.assertEqual(brain_increase, 1)

if __name__ == '__main__':
    unittest.main()
