from ai_brain.brain import Brain
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class AiBrainImporter(ABC):
    brain = None

    def __init__(self, brain: Brain):
        self.brain = brain

    @abstractmethod
    def do_import(self):
        pass

    @abstractmethod
    def get_params(self):
        pass

