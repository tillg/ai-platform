import json
import unittest
import uuid
from ai_brain.brain import Brain
from ai_commons.apiModelsSearch import BrainParameters, Document
import logging
import os
import string
import random
from ai_commons.constants import TEST_DATA_DIRECTORY, TMP_DATA_DIRECTORY
from utils.utils import get_now_as_string, simplify_text, get_test_filename

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

LONG_ARTICLE = "wikipedia_peru.txt"
SHORT_ARTICLE = "rectus_abdominus.txt"


def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for i in range(length))


class TestBrain(unittest.TestCase):

    def test_brain_initialization(self):
<<<<<<< HEAD
        brain_parameters = BrainParameters(brain_id="whatever",
                                           name="whatever",
                                           description="whatever",
                                           data_directory=get_test_filename(TMP_DATA_DIRECTORY),
                                           scraper=None,
                                           allow_duplicates=True)
=======
        brain_parameters = BrainParameters(
            brain_id="whatever",
            name="whatever",
            description="whatever",
            data_directory=get_test_filename(TMP_DATA_DIRECTORY),
            scraper=None,
            allow_duplicates=True,
        )
>>>>>>> gitbutler/integration

        brain = Brain(brain_parameters)
        self.assertIsInstance(
            brain, Brain, "Brain object is not an instance of Brain class"
        )

    def test_brain_import_doc(self):
<<<<<<< HEAD
        brain_parameters = BrainParameters(brain_id="whatever",
                                           name="whatever",
                                           description="whatever",
                                           data_directory=get_test_filename(
                                               TMP_DATA_DIRECTORY),
                                           scraper=None,
                                           allow_duplicates=True)
=======
        brain_parameters = BrainParameters(
            brain_id="whatever",
            name="whatever",
            description="whatever",
            data_directory=get_test_filename(TMP_DATA_DIRECTORY),
            scraper=None,
            allow_duplicates=True,
        )
>>>>>>> gitbutler/integration
        brain = Brain(brain_parameters)
        brain_size_pre = brain.number_of_documents()
        doc = Document.from_text_file(os.path.join(TEST_DATA_DIRECTORY, LONG_ARTICLE))
        brain.import_document(doc)
        brain_size_post = brain.number_of_documents()
        self.assertEqual(brain_size_post - brain_size_pre, 1)

    def test_brain_import_multiple_docs(self):
<<<<<<< HEAD
        brain_parameters = BrainParameters(brain_id="whatever",
                                           name="whatever",
                                           description="whatever",
                                           data_directory=get_test_filename(
                                               TMP_DATA_DIRECTORY),
                                           scraper=None,
                                           allow_duplicates=True)
=======
        brain_parameters = BrainParameters(
            brain_id="whatever",
            name="whatever",
            description="whatever",
            data_directory=get_test_filename(TMP_DATA_DIRECTORY),
            scraper=None,
            allow_duplicates=True,
        )
>>>>>>> gitbutler/integration
        brain = Brain(brain_parameters)
        brain.delete_all()
        brain_size_pre = brain.number_of_documents()
        doc1 = Document.from_text_file(os.path.join(TEST_DATA_DIRECTORY, LONG_ARTICLE))
        doc2 = Document.from_text_file(os.path.join(TEST_DATA_DIRECTORY, SHORT_ARTICLE))
        brain.import_documents([doc1, doc2])
        brain_size_post = brain.number_of_documents()
        self.assertEqual(brain_size_post - brain_size_pre, 2)

    def test_brain_get_doc_by_id(self):
<<<<<<< HEAD
        brain_parameters = BrainParameters(brain_id="whatever",
                                           name="whatever",
                                           description="whatever",
                                           data_directory=get_test_filename(
                                               TMP_DATA_DIRECTORY),
                                           scraper=None,
                                           allow_duplicates=True)
=======
        brain_parameters = BrainParameters(
            brain_id="whatever",
            name="whatever",
            description="whatever",
            data_directory=get_test_filename(TMP_DATA_DIRECTORY),
            scraper=None,
            allow_duplicates=True,
        )
>>>>>>> gitbutler/integration

        brain = Brain(brain_parameters)
        doc = Document.from_text_file(os.path.join(TEST_DATA_DIRECTORY, SHORT_ARTICLE))
        brain.import_document(doc)
        doc_id = doc.id
        doc_retrieved = brain.get_document_by_id(doc_id)
        self.assertEqual(doc, doc_retrieved)

    def test_brain_get_doc_by_uri(self):
<<<<<<< HEAD
        brain_parameters = BrainParameters(brain_id="whatever",
                                           name="whatever",
                                           description="whatever",
                                           data_directory=get_test_filename(
                                               TMP_DATA_DIRECTORY),
                                           scraper=None,
                                           allow_duplicates=True)
=======
        brain_parameters = BrainParameters(
            brain_id="whatever",
            name="whatever",
            description="whatever",
            data_directory=get_test_filename(TMP_DATA_DIRECTORY),
            scraper=None,
            allow_duplicates=True,
        )
>>>>>>> gitbutler/integration
        brain = Brain(brain_parameters)
        doc = Document.from_text_file(os.path.join(TEST_DATA_DIRECTORY, SHORT_ARTICLE))
        doc.uri = generate_random_string(10)
        brain.import_document(doc)
        doc_retrieved = brain.get_document_by_uri(doc.uri)
        self.assertEqual(doc, doc_retrieved)

    def test_brain_delete_all(self):
<<<<<<< HEAD
        brain_parameters = BrainParameters(brain_id="whatever",
                                           name="whatever",
                                           description="whatever",
                                           data_directory=get_test_filename(
                                               TMP_DATA_DIRECTORY),
                                           scraper=None,
                                           allow_duplicates=True)
=======
        brain_parameters = BrainParameters(
            brain_id="whatever",
            name="whatever",
            description="whatever",
            data_directory=get_test_filename(TMP_DATA_DIRECTORY),
            scraper=None,
            allow_duplicates=True,
        )
>>>>>>> gitbutler/integration

        brain = Brain(brain_parameters)
        doc = Document.from_text_file(os.path.join(TEST_DATA_DIRECTORY, SHORT_ARTICLE))
        brain.import_document(doc)
        brain.delete_all()
        self.assertEqual(brain.number_of_documents(), 0)

    def test_brain_delete_all_and_then_add_a_doc(self):
<<<<<<< HEAD
        brain_parameters = BrainParameters(brain_id="whatever",
                                           name="whatever",
                                           description="whatever",
                                           data_directory=get_test_filename(
                                               TMP_DATA_DIRECTORY),
                                           scraper=None,
                                           allow_duplicates=True)
=======
        brain_parameters = BrainParameters(
            brain_id="whatever",
            name="whatever",
            description="whatever",
            data_directory=get_test_filename(TMP_DATA_DIRECTORY),
            scraper=None,
            allow_duplicates=True,
        )
>>>>>>> gitbutler/integration

        brain = Brain(brain_parameters)
        doc = Document.from_text_file(os.path.join(TEST_DATA_DIRECTORY, SHORT_ARTICLE))
        brain.import_document(doc)
        brain.delete_all()
        self.assertEqual(brain.number_of_documents(), 0)
        brain.import_document(doc)
        self.assertEqual(brain.number_of_documents(), 1)

    def test_import_doc_without_duplicate(self):
<<<<<<< HEAD
        brain_parameters = BrainParameters(brain_id="whatever",
                                           name="whatever",
                                           description="whatever",
                                           data_directory=get_test_filename(
                                               TMP_DATA_DIRECTORY),
                                           scraper=None,
                                           allow_duplicates=True)
=======
        brain_parameters = BrainParameters(
            brain_id="whatever",
            name="whatever",
            description="whatever",
            data_directory=get_test_filename(TMP_DATA_DIRECTORY),
            scraper=None,
            allow_duplicates=True,
        )
>>>>>>> gitbutler/integration

        brain = Brain(brain_parameters)
        brain.delete_all()
        pre_size = brain.number_of_documents()
        doc = Document.from_text_file(os.path.join(TEST_DATA_DIRECTORY, SHORT_ARTICLE))
        brain.import_document(doc)
        brain.import_document(doc)
        brain_increase = brain.number_of_documents() - pre_size
        self.assertEqual(brain_increase, 1)

    def test_get_params(self):
<<<<<<< HEAD
        brain_parameters = BrainParameters(brain_id="whatever",
                                           name="whatever",
                                           description="whatever",
                                           data_directory=get_test_filename(
                                               TMP_DATA_DIRECTORY),
                                           scraper=None,
                                           allow_duplicates=True)
=======
        brain_parameters = BrainParameters(
            brain_id="whatever",
            name="whatever",
            description="whatever",
            data_directory=get_test_filename(TMP_DATA_DIRECTORY),
            scraper=None,
            allow_duplicates=True,
        )
>>>>>>> gitbutler/integration

        brain = Brain(brain_parameters)
        params = brain.get_parameters()
        self.assertIn("data_directory", params)
        self.assertIn("allow_duplicates", params)
        formatted_params = json.dumps(params, indent=4)
        logger.info(f"Params: {formatted_params}")

    def test_get_brain_list(self):
        brains_list = Brain.get_brain_parameters_list(
            brains_index_file=os.path.join(TEST_DATA_DIRECTORY, "brains.json")
        )
        logging.info(brains_list)
        self.assertTrue(len(brains_list) > 0)

    def test_get_default_brain(self):
        brains_index_file = os.path.join(TEST_DATA_DIRECTORY, "brains.json")
        logger.info(f"test_get_default_brain: Reading from brains index file: {
                    brains_index_file}")
        brain = Brain.get_default_brain(brains_index_file=brains_index_file)
        brain_name = brain.get_parameters()["name"]
        self.assertIsInstance(
            brain, Brain, "Default brain is not an instance of Brain class"
        )
        self.assertEqual(brain_name, "Mathematics")

    def test_get_default_brain_without_default(self):
        brain = Brain.get_default_brain(
            brains_index_file=os.path.join(
                TEST_DATA_DIRECTORY, "brains_with_no_default.json"
            )
        )
        self.assertIsInstance(
            brain, Brain, "Default brain is not an instance of Brain class"
        )
        brain_name = brain.get_parameters()["name"]
        self.assertEqual(brain_name, "Berlin")


if __name__ == "__main__":
    unittest.main()
