import json
import unittest
import uuid
from ai_brain.brain import Brain
from ai_brain.brain_scraper_factory import BrainScraperFactory
from ai_commons.apiModelsSearch import Document, Chunk
import logging
import os
import string
import random
from utils.utils import get_now_as_string, simplify_text
from ai_brain.brain_scraper_wikipedia import BrainScraperWikipedia

logging.basicConfig(level=logging.WARNING)
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
            TMP_DATA_DIR, simplify_text(get_now_as_string()+'_test_wikipedia_save_page'))
        doc: Document = scraper._get_page_as_document_and_links(
            WIKIPEDIA_PAGE, "en")
        doc.document.write_2_json(test_dir)

    def test_scrape_page(self):
        parameters = {"start_page_title": WIKIPEDIA_PAGE,
                      "target_dir": os.path.join(
                          TMP_DATA_DIR, simplify_text(get_now_as_string()+'_test_scrape_page')),
                      "depth": 1}
        scraper = BrainScraperWikipedia(parameters=parameters)
        params = scraper.get_parameters()
        formatted_params = json.dumps(params, indent=4)
        logger.info(f"Scraper params: {formatted_params}")
        scraper.do_scrape()
        # self.assertTrue(len(brain) > 0)
        # logger.info(f"Brain info: {json.dumps(brain.get_params_and_stats(), indent=4)}")

    def test_scraper_by_factory(self):
        parameters = {"scraper_type": "wikipedia",
                      "start_page_title": WIKIPEDIA_PAGE,
                      "target_dir": os.path.join(
                          TMP_DATA_DIR, simplify_text(get_now_as_string()+'_test_scrape_page')),
                      "depth": 1}
        scraper = BrainScraperFactory().create_brain_scraper(parameters)
        self.assertIsInstance(scraper, BrainScraperWikipedia)

    def test_scraper_by_brain_definition(self):
        brain = Brain.get_brain_by_id("scraper_test", brains_index_filename=os.path.join(
            TEST_DATA_DIR, "brains.json"))
        scraper = brain.get_scraper()
        self.assertIsInstance(scraper, BrainScraperWikipedia)


if __name__ == '__main__':
    unittest.main()
