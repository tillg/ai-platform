import unittest
import os
import logging
from ai_commons.constants import SRC_DIRECTORY

logging.basicConfig(level=logging.INFO)

brain_cli = os.path.join(SRC_DIRECTORY, "ai_cli/brain")
print(brain_cli)

# Configure logging
logging.basicConfig(level=logging.INFO)


class TestCli(unittest.TestCase):

    def test_list(self):
        exit_status = os.system(f"{brain_cli} list")
        assert exit_status == 0


if __name__ == '__main__':
    unittest.main()
