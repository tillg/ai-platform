import json
import unittest
import uuid
from ai_brain.brain import Brain
from ai_commons.apiModelsSearch import BrainParameters, Document
import logging
import os
import string
import random
from ai_commons.constants import TEST_DATA_DIR, TMP_DATA_DIR
from utils.utils import get_now_as_string

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LONG_ARTICLE = "wikipedia_peru.txt"
SHORT_ARTICLE = "rectus_abdominus.txt"

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

class TestBrain(unittest.TestCase):

    def test_brain_initialization(self):
        brain_parameters = BrainParameters(id="whatever",
                                           name="whatever",
                                           description="whatever",
                                           data_directory=TMP_DATA_DIR,
                                           scraper=None,
                                           allow_duplicates=True,
                                           path=get_now_as_string()+'_test_brain')

        brain = Brain(brain_parameters)

    def test_brain_import_doc(self):
        brain_parameters = BrainParameters(id="whatever",
                                           name="whatever",
                                           description="whatever",
                                           data_directory=TMP_DATA_DIR,
                                           scraper=None,
                                           allow_duplicates=True,
                                           path=get_now_as_string()+'_test_brain')
        brain = Brain(brain_parameters)
        brain_size_pre = brain.number_of_documents()
        doc = Document.from_text_file(os.path.join(
            TEST_DATA_DIR, LONG_ARTICLE))
        brain.import_document(doc)
        brain_size_post = brain.number_of_documents()
        self.assertEqual(brain_size_post-brain_size_pre, 1)

    def test_brain_import_multiple_docs(self):
        brain_parameters = BrainParameters(id="whatever",
                                           name="whatever",
                                           description="whatever",
                                           data_directory=TMP_DATA_DIR,
                                           scraper=None,
                                           allow_duplicates=True,
                                           path=get_now_as_string()+'_test_brain')
        brain = Brain(brain_parameters)
        brain.delete_all()
        brain_size_pre = brain.number_of_documents()
        doc1 = Document.from_text_file(os.path.join(
            TEST_DATA_DIR, LONG_ARTICLE))
        doc2 = Document.from_text_file(os.path.join(
            TEST_DATA_DIR, SHORT_ARTICLE))
        brain.import_documents([doc1, doc2])
        brain_size_post = brain.number_of_documents()
        self.assertEqual(brain_size_post-brain_size_pre, 2)

    def test_brain_get_doc_by_id(self):
        brain_parameters = BrainParameters(id="whatever",
                                           name="whatever",
                                           description="whatever",
                                           data_directory=TMP_DATA_DIR,
                                           scraper=None,
                                           allow_duplicates=True,
                                           path=get_now_as_string()+'_test_brain')

        brain = Brain(brain_parameters)
        doc = Document.from_text_file(os.path.join(
            TEST_DATA_DIR, SHORT_ARTICLE))
        brain.import_document(doc)
        doc_id = doc.id
        doc_retrieved = brain.get_document_by_id(doc_id)
        self.assertEqual(doc, doc_retrieved)

    def test_brain_get_doc_by_uri(self):
        brain_parameters = BrainParameters(id="whatever",
                                           name="whatever",
                                           description="whatever",
                                           data_directory=TMP_DATA_DIR,
                                           scraper=None,
                                           allow_duplicates=True,
                                           path=get_now_as_string()+'_test_brain')
        brain = Brain(brain_parameters)
        doc = Document.from_text_file(os.path.join(
            TEST_DATA_DIR, SHORT_ARTICLE))
        doc.uri = generate_random_string(10)
        brain.import_document(doc)
        doc_retrieved = brain.get_document_by_uri(doc.uri)
        self.assertEqual(doc, doc_retrieved)

    def test_brain_delete_all(self):
        brain_parameters = BrainParameters(id="whatever",
                                           name="whatever",
                                           description="whatever",
                                           data_directory=TMP_DATA_DIR,
                                           scraper=None,
                                           allow_duplicates=True,
                                           path=get_now_as_string()+'_test_brain')

        brain = Brain(brain_parameters)
        doc = Document.from_text_file(os.path.join(
            TEST_DATA_DIR, SHORT_ARTICLE))
        brain.import_document(doc)
        brain.delete_all()
        self.assertEqual(brain.number_of_documents(), 0)

    def test_brain_delete_all_and_then_add_a_doc(self):
        brain_parameters = BrainParameters(id="whatever",
                                           name="whatever",
                                           description="whatever",
                                           data_directory=TMP_DATA_DIR,
                                           scraper=None,
                                           allow_duplicates=True,
                                           path=get_now_as_string()+'_test_brain')

        brain = Brain(brain_parameters)
        doc = Document.from_text_file(os.path.join(
            TEST_DATA_DIR, SHORT_ARTICLE))
        brain.import_document(doc)
        brain.delete_all()
        self.assertEqual(brain.number_of_documents(), 0)
        brain.import_document(doc)
        self.assertEqual(brain.number_of_documents(), 1)

    def test_import_doc_without_duplicate(self):
        brain_parameters = BrainParameters(id="whatever",
                                           name="whatever",
                                           description="whatever",
                                           data_directory=TMP_DATA_DIR,
                                           scraper=None,
                                           allow_duplicates=True,
                                           path=get_now_as_string()+'_test_brain')

        brain = Brain(brain_parameters)
        brain.delete_all()
        pre_size = brain.number_of_documents()
        doc = Document.from_text_file(os.path.join(
            TEST_DATA_DIR, SHORT_ARTICLE))
        brain.import_document(doc)
        brain.import_document(doc)
        brain_increase = brain.number_of_documents() - pre_size
        self.assertEqual(brain_increase, 1)

    def test_get_params(self):
        brain_parameters = BrainParameters(id="whatever",
                                           name="whatever",
                                           description="whatever",
                                           data_directory=TMP_DATA_DIR,
                                           scraper=None,
                                           allow_duplicates=True,
                                           path=get_now_as_string()+'_test_brain')

        brain = Brain(brain_parameters)
        params = brain.get_parameters()
        self.assertIn("data_directory", params)
        self.assertIn("path", params)
        self.assertIn("allow_duplicates", params)
        formatted_params = json.dumps(params, indent=4)
        logger.info(f"Params: {formatted_params}")

    def test_get_brain_list(self):
        brains_list = Brain.get_brain_parameters_list(brains_index_file=os.path.join(
            TEST_DATA_DIR, "brains.json"))
        logging.info(brains_list)
        self.assertTrue(len(brains_list) > 0)

    def test_get_default_brain_name(self):
        brain = Brain.get_default_brain_id(brains_index_file=os.path.join(
            TEST_DATA_DIR, "brains.json"))
        brain_name = brain.get_parameters()["name"]
        self.assertEqual(brain_name, "Mathematics")

    def test_get_default_brain_name_without_default(self):
        brain = Brain.get_default_brain_id(brains_index_file=os.path.join(
            TEST_DATA_DIR, "brains_with_no_default.json"))
        brain_name = brain.get_parameters()["name"]
        self.assertEqual(brain_name, "Berlin")

if __name__ == '__main__':
    unittest.main()
