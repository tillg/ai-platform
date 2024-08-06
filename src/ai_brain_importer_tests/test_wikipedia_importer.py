import json
import unittest
import uuid
from ai_brain.brain import Brain
from ai_commons.apiModelsSearch import Document, Chunk
import logging
from dotenv import load_dotenv
import os
import string
import random
from ai_brain_importer.ai_brain_importer_wikipedia import AiBrainImporterWikipedia
from utils.utils import get_now_as_string
from ai_brain_importer.brain_importer_factory import BrainImporterFactory

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# in relation to this file my test data resides in ../../data/test_data
TEST_DATA_DIR = os.path.join(os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))), "data", "test_data")
TMP_DATA_DIR = os.path.join(os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))), "data", "tmp")

WIKIPEDIA_PAGE = "Berlin"

class TestWikipedia_loader(unittest.TestCase):

    def test_save_page_as_doc(self):
        brain = Brain({"data_directory": TMP_DATA_DIR,
                       "path": get_now_as_string()+'_test_wikipedia_save_page',
                       "allow_duplicates": False})
        importer = AiBrainImporterWikipedia(brain, {"start_page_title": WIKIPEDIA_PAGE})
        test_dir = os.path.join(
            TMP_DATA_DIR, get_now_as_string()+'_test_wikipedia_save_page')
        doc: Document = importer._get_page_as_document_and_links(WIKIPEDIA_PAGE, "en")
        doc.document.write_2_file(test_dir)

    def test_import_page(self):
        brain = Brain({"data_directory": TMP_DATA_DIR,
                       "path": get_now_as_string()+'_test_wikipedia_import_page',
                       "allow_duplicates": False})
        importer = AiBrainImporterWikipedia(brain, {"start_page_title": WIKIPEDIA_PAGE, "depth":1})
        params = importer.get_params()
        formatted_params = json.dumps(params, indent=4)
        logger.info(f"Importer params: {formatted_params}")
        importer.do_import()
        self.assertTrue(len(brain) > 0)
        logger.info(f"Brain info: {json.dumps(brain.get_params_and_stats(), indent=4)}")

    def test_importer_by_factory(self):
        brain = Brain({"data_directory": TMP_DATA_DIR,
                       "path": get_now_as_string()+'_test_wikipedia_importer_by_factory',
                       "allow_duplicates": False})
        importer_factory = BrainImporterFactory()
        importer_params = {"start_page_title": WIKIPEDIA_PAGE, "depth": 1}
        importer = importer_factory.create_brain_importer(brain, importer_params)
        importer.do_import()
        self.assertTrue(len(brain) == 1)

if __name__ == '__main__':
    unittest.main()
