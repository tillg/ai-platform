from typing import Any, Dict
import logging
from abc import ABC, abstractmethod
import os

from utils.dict2file import read_dict_from_file, write_dict_to_file
from utils.utils import get_now_as_string

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

INDEX_FILENAME = "_scrape_index.json"

class BrainScraper(ABC):
    brain = None

    def __init__(self, parameters):
        self.parameters = parameters

        # Check that we have a target_dir
        if "target_dir" not in parameters:
            raise ValueError("target_dir is required for Brain Scraper.")
        
        # Set some defaults
        self.parameters["index_filename"] = os.path.join(
            self.parameters["target_dir"], INDEX_FILENAME)
        self.index = {}
        if os.path.exists(self.parameters["index_filename"]):
            return read_dict_from_file(full_filename=self.parameters["index_filename"])

    @abstractmethod
    def do_scrape(self):
        self.parameters["last_scrape"] = get_now_as_string()
        write_dict_to_file(dictionary=self.parameters, full_filename=self.parameters["index_filename"])

    def get_parameters(self) -> Dict[str, Any]:
        return self.parameters
    
    def get_statistics(self) -> Dict[str, Any]:
        # TODO: Return at least the number of docs in the target_dir
        return self.index
