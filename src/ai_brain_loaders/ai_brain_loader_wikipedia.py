from fastapi import Depends, FastAPI
import uvicorn

import ai_brain.api_routes
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


def create_brain(data_directory: str, start_page_title: str, language: str = 'en', depth: int = 2) -> Brain:
    brain = Brain(data_directory=data_directory)
    load_page_tree_to_brain(
        brain=brain, start_page_title=start_page_title, language=language, depth=depth)
    return brain


def load_page_tree_to_brain(brain: Brain, start_page_title: str = "Berlin", language: str = 'en', depth: int = 2):
    document_and_links = _get_page_as_document_and_links(
        page_title=start_page_title, language=language)
    brain.add_document(document_and_links.document)
    if depth > 1:
        for page in document_and_links.links:
            load_page_tree_to_brain(
                brain=brain,
                start_page_title=page,
                language=language,
                depth=depth-1
            )


def _get_page_as_document_and_links(page_title: str, language: str = 'en'):
    wiki = wikipediaapi.Wikipedia(
        user_agent='brain_loader_bot/0.1 (till.gartner@gmail.com) WikipediaAPI Python',
        language=language,
        extract_format=wikipediaapi.ExtractFormat.WIKI
    )
    page = wiki.page(page_title)
    if not page.exists():
        logger.warning(f"Page {page_title} in {language} does not exist.")
        return None
    document = Document(
        title=page_title,
        uri=page.canonicalurl,
        content=page.text)
    links = list(page.links.keys())
    return SimpleNamespace(document=document, links=links)
