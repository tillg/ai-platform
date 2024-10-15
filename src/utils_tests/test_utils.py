import unittest
from utils.utils import get_now_as_string, simplify_text
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class TestUtils(unittest.TestCase):

    def test_simplify_text(self):
        original = "2024-09-17 08:11:06_chunks"
        simplified = simplify_text(original)
        logger.info(f"simplified: {simplified}")
        self.assertEqual(simplified, "2024-09-17_08_11_06_chunks")
