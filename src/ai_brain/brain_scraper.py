from ai_brain.brain import Brain
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class BrainScraper(ABC):
    brain = None

    def __init__(self, parameters):
        self.parameters = parameters

        # Chat that we have a target_dir
        if "target_dir" not in parameters:
            raise ValueError("target_dir is required for Brain Scraper.")

    @abstractmethod
    def do_scrape(self):
        pass

    @abstractmethod
    def get_parameters(self):
        pass
