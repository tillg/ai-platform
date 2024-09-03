import random

import logging
from typing import Any, Dict

import wikipediaapi
from ai_commons.apiModelsSearch import Document
from types import SimpleNamespace
from ai_brain.brain_scraper import BrainScraper

logger = logging.getLogger(__name__)
LOG_LEVEL_FOR_IMPORT = logging.WARN

logger.setLevel(LOG_LEVEL_FOR_IMPORT)
wikipediaapi_logger = logging.getLogger('wikipediaapi')
wikipediaapi_logger.setLevel(LOG_LEVEL_FOR_IMPORT)

class BrainScraperWikipedia(BrainScraper):

    def __init__(self, parameters: Dict[str, Any]):
        super().__init__(parameters=parameters)

        if "start_page_title" not in parameters:
            raise ValueError("start_page_title is required for Wikipedia Importer.")

        # Complete some parameters with defaults
        self.parameters["language"] = parameters.get("language", 'en')
        self.parameters["depth"] = parameters.get("depth", 2)
        self.parameters["max_no_of_docs"] = parameters.get("max_no_of_docs", 0)

    def do_scrape(self):
        self._load_wikipedia_page_tree(
            start_page_title=self.parameters["start_page_title"],
            language=self.parameters["language"],
            depth=self.parameters["depth"]
        )

    def _load_wikipedia_page_tree(self, start_page_title: str, language: str = 'en', depth: int = 2):
        document_and_links = self._get_page_as_document_and_links(
            page_title=start_page_title, language=language)
        if document_and_links is None:
            logger.warning(f"Page '{start_page_title}' in '{language}' was not retrieved.")
        else:
            document = document_and_links.document
            document.write_2_file(self.parameters["target_dir"])
        if depth > 1:
            random.shuffle(document_and_links.links)
            for page in document_and_links.links:
                if self.parameters["max_no_of_docs"] > 0 and len(self.brain) >= self.parameters["max_no_of_docs"]:
                    logger.info(
                        f"Ingestion reached max no of docs: {self.max_no_of_docs}")
                    return
                try:
                    print(".", end="", flush=True)
                    self._load_wikipedia_page_tree(
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

    def get_parameters(self):
        return self.parameters