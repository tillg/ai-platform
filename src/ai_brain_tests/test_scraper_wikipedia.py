import json
import unittest
import uuid
from ai_commons.apiModelsSearch import Document, Chunk
import logging
import os
import string
import random
from utils.utils import get_now_as_string
from ai_brain.brain_scraper_wikipedia import BrainScraperWikipedia

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# in relation to this file my test data resides in ../../data/test_data
TEST_DATA_DIR = os.path.join(os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))), "data", "test_data")
TMP_DATA_DIR = os.path.join(os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))), "data", "tmp")

WIKIPEDIA_PAGE = "Berlin"

class TestWikipediaScraper(unittest.TestCase):

    def test_save_page_as_doc(self):
        parameters = {"start_page_title": WIKIPEDIA_PAGE,
                      "target_dir": TMP_DATA_DIR}
        scraper = BrainScraperWikipedia(parameters=parameters)
        test_dir = os.path.join(
            TMP_DATA_DIR, get_now_as_string()+'_test_wikipedia_save_page')
        doc: Document = scraper._get_page_as_document_and_links(WIKIPEDIA_PAGE, "en")
        doc.document.write_2_json(test_dir)

    def test_scrape_page(self):
        parameters = {"start_page_title": WIKIPEDIA_PAGE,
                      "target_dir": TMP_DATA_DIR,
                      "depth": 1}
        scraper = BrainScraperWikipedia(parameters=parameters)
        params = scraper.get_parameters()
        formatted_params = json.dumps(params, indent=4)
        logger.info(f"Importer params: {formatted_params}")
        scraper.do_scrape()
        # self.assertTrue(len(brain) > 0)
        # logger.info(f"Brain info: {json.dumps(brain.get_params_and_stats(), indent=4)}")

    # def test_scraper_by_factory(self):
    #     importer_factory = BrainImporterFactory()
    #     importer_params = {"start_page_title": WIKIPEDIA_PAGE, "depth": 1}
    #     importer = importer_factory.create_brain_importer(brain, importer_params)
    #     importer.do_import()
    #     self.assertTrue(len(brain) == 1)

if __name__ == '__main__':
    unittest.main()
