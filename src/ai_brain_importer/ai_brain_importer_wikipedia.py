import random

import logging
from typing import Any, Dict

from pydantic import validate_call
import ai_commons.constants as constants
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import wikipediaapi
from ai_brain.brain import Brain
from ai_commons.apiModelsSearch import Document
from types import SimpleNamespace
from ai_brain_importer.ai_brain_importer import AiBrainImporter

load_dotenv()
logger = logging.getLogger(__name__)
LOG_LEVEL_FOR_IMPORT = logging.WARN

logger.setLevel(LOG_LEVEL_FOR_IMPORT)
wikipediaapi_logger = logging.getLogger('wikipediaapi')
wikipediaapi_logger.setLevel(LOG_LEVEL_FOR_IMPORT)

class AiBrainImporterWikipedia(AiBrainImporter):

    def __init__(self, brain: Brain, params: Dict[str, Any]):
        super().__init__(brain)

        self.params = params.copy()
        self.original_params = params.copy()

        if "start_page_title" not in params:
            raise ValueError("start_page_title is required for Wikipedia Importer.")
        self.start_page_title = params.get("start_page_title")

        self.language = params.get("language", 'en')
        self.params["language"] = self.language

        self.depth = params.get("depth", 2)
        self.params["depth"] = self.depth

        self.max_no_of_docs = params.get("max_no_of_docs", 0)
        self.params["max_no_of_docs"] = self.max_no_of_docs

    def do_import(self):
        self.load_wikipedia_page_tree(
            start_page_title=self.start_page_title,
            language=self.language,
            depth=self.depth
        )

    def load_wikipedia_page_tree(self, start_page_title: str, language: str = 'en', depth: int = 2):
        document_and_links = self._get_page_as_document_and_links(
            page_title=start_page_title, language=language)
        if document_and_links is None:
            logger.warning(f"Page '{start_page_title}' in '{language}' was not retrieved.")
        else:
            self.brain.import_document(document_and_links.document)
            if len(self.brain) % 10 == 0:
                print(f"[Brain: {len(self.brain)}]",
                      end="", flush=True)
        if depth > 1:
            random.shuffle(document_and_links.links)
            for page in document_and_links.links:
                if self.max_no_of_docs > 0 and len(self.brain) >= self.max_no_of_docs.max_no_of_docs:
                    logger.info(
                        f"Ingestion reached max no of docs: {self.max_no_of_docs}")
                    return
                try:
                    print(".", end="", flush=True)
                    self.load_wikipedia_page_tree(
                            start_page_title=page,
                            language=language,
                            depth=depth-1
                        )
                except Exception as e:
                    logger.error(f"Error loading page tree for {page}: {str(e)}")
        return


    def _get_page_as_document_and_links(self, page_title: str, language: str):
        try:
            wiki = wikipediaapi.Wikipedia(
                user_agent='brain_loader_bot/0.1 (till.gartner@gmail.com) WikipediaAPI Python',
                language=language,
                extract_format=wikipediaapi.ExtractFormat.WIKI,
                timeout=30
            )
            page = wiki.page(page_title)
        except Exception as e:
            logger.error(f"Error loading page {page_title} in '{language}': {str(e)}")
            # raise
        if not page.exists():
            logger.error(f"Page '{page_title}' in '{language}' does not exist.")
            return None
            # raise Exception(f"Page {page_title} in {language} does not exist.")    
        document = Document(
            title=page_title,
            uri=page.canonicalurl,
            content=page.text)
        links = list(page.links.keys())
        return SimpleNamespace(document=document, links=links)

    def get_params(self):
        return self.params