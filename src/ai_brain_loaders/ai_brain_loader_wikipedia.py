from fastapi import Depends, FastAPI
import uvicorn
import random

import ai_brain.brain_api_routes
import logging
import ai_commons.constants as constants
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
import wikipediaapi
from ai_brain.brain import Brain
from ai_commons.api_models import Document
from types import SimpleNamespace

load_dotenv()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def load_page_tree_to_brain(brain: Brain, start_page_title: str = "Berlin", language: str = 'en', depth: int = 2):
    document_and_links = _get_page_as_document_and_links(
        page_title=start_page_title, language=language)
    brain.add_document(document_and_links.document)
    if depth > 1:
        random.shuffle(document_and_links.links)
        for page in document_and_links.links:
            if brain.max_no_of_docs > 0 and len(brain) >= brain.max_no_of_docs:
                logger.info(
                    f"Brain reached max no of docs: {brain.max_no_of_docs}")
                return
            try:
                load_page_tree_to_brain(
                        brain=brain,
                        start_page_title=page,
                        language=language,
                        depth=depth-1
                    )
            except Exception as e:
                logger.error(f"Error loading page tree for {page}: {str(e)}")
                return


def _get_page_as_document_and_links(page_title: str, language: str = 'en'):
    try:
        wiki = wikipediaapi.Wikipedia(
            user_agent='brain_loader_bot/0.1 (till.gartner@gmail.com) WikipediaAPI Python',
            language=language,
            extract_format=wikipediaapi.ExtractFormat.WIKI,
            timeout=30
        )
        page = wiki.page(page_title)
    except Exception as e:
        logger.error(f"Error loading page {page_title} in {language}: {str(e)}")
        raise
    if not page.exists():
        logger.warning(f"Page {page_title} in {language} does not exist.")
        raise Exception(f"Page {page_title} in {language} does not exist.")    
    document = Document(
        title=page_title,
        uri=page.canonicalurl,
        content=page.text)
    links = list(page.links.keys())
    return SimpleNamespace(document=document, links=links)
