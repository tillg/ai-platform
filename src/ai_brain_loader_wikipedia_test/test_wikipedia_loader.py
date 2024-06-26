import unittest
import uuid
from ai_brain.brain import Brain
from ai_commons.api_models import Document, Chunk
import logging
from dotenv import load_dotenv
import os
import string
import random
from ai_brain_loaders.ai_brain_loader_wikipedia import _get_page_as_document_and_links, create_brain
from utils.utils import get_now_as_string

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
        test_dir = os.path.join(
            TMP_DATA_DIR, get_now_as_string()+'_test_wikipedia_doc')
        doc: Document = _get_page_as_document_and_links(WIKIPEDIA_PAGE)
        doc.document.write_2_file(test_dir)

    def test_create_brain(self):
        brain_directory = os.path.join(TMP_DATA_DIR, get_now_as_string()+'_test_brain')
        brain = create_brain(data_directory=brain_directory,
                             start_page_title=WIKIPEDIA_PAGE)
        logger.info(str(brain))

