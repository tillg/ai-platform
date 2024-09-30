import json
import unittest
import logging
from ai_commons.constants import TEST_DATA_DIRECTORY, PROJECT_ROOT
import os
from utils.dict2file import read_dict_from_template_file

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class TestDict2File(unittest.TestCase):

    def test_read_dict_from_template_file(self):

        json_filename_with_template = os.path.join(TEST_DATA_DIRECTORY, "test_template.json")
        read_dict = read_dict_from_template_file(full_filename=json_filename_with_template)
        print(json.dumps(read_dict, indent=2))
        self.assertIsInstance(read_dict["berlin"]["project_root"], str)
        self.assertIsInstance(PROJECT_ROOT, str)
        self.assertEqual(read_dict["berlin"]["project_root"], PROJECT_ROOT)


