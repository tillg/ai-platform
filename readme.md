# AI-Platform 
An AI Platform for tinkering.

[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

__Table of contents__

- [AI-Platform](#ai-platform)
  - [Developer Guide](#developer-guide)
    - [Installing](#installing)
    - [Running](#running)
    - [Running the tests](#running-the-tests)
  - [The Brains](#the-brains)
  - [The Prompts](#the-prompts)
  - [Use cases](#use-cases)
  - [Code hygiene](#code-hygiene)
  - [TODO](#todo)
  - [DONE](#done)
  - [Resources](#resources)
  - [Things to look at](#things-to-look-at)

![Overview](ai_platform_overview.svg)

## Developer Guide

### Installing


__Prerequisites__:

* Python 3.12
* [Poetry](https://python-poetry.org/)

To setup the backend run `poetry install` and you are done ;) 

For the frontend:
```
cd src/ai_ui
npm install
```

### Running

Run the backend components:

```bash
# Chains
ai_chains

# LLM Wrapper
llm_wraper

# Brains
ai_brain
```

To start all the backend components at once there is a script:
```bash
cd src
./start_backend.sh
```

Run the UI:
```bash
cd src/ai_ui_a12
npm start
```

### Running the tests


For the backend tests:
```bash
cd src

# Run the tests of one compnenent, for example ai_commons
python -m unittest discover ai_commons_tests

# Run all the unit tests
python -m unittest discover . 
```

For the UI tests:
```bash
cd src/ui
npm test
```

## The Brains

A brain is a Vectore Database (or a namespace within a vector DB) that contains documents / embeddings about a certain domain. It is typically attached to a pipeline that configures what data is to be loaded from where.

Technically the Brain contains 2 data storages and one index file:

* `documents`: This is a directory with json files, one for each document.
* `chroma`: This is a directory that contains the ChromaDB with the indexes of the chunks.
* `_index.json` contains a list of all the files in `documents` with some meta data - most notably the URI pointing to the initial location of that document.

Filling a brain with consists of the following steps:

* **`scraper`** imports the documents. THis is typically done by a scraping process. We provide different `brain_scraper`:
  * `brain_scraper_wikipedia`
  * `brain_scraper_confluence`
* **Chunking** consists of cutting the documents into digestable pieces. We plan to have different chunking strategies, currently we have 
  * `ChunkerCharacterTextSplitter` that simply cuts text into equal length chunks.
* **Indexing**, that calculates embeddings and adds those embeddings to the vector database. Currently we only have one way of calculating embedding:
  * the default of [ChromaDB](https://www.trychroma.com) that is the [all-MiniLM-L6-v2](https://docs.trychroma.com/guides/embeddings#default:-all-minilm-l6-v2)

These steps are performed/triggered by the `brain` itself. So the brain has 
* a scraper
* a chunker
* an indexer that calculates embeddings and has a vector DB.

The different steps can also be run independenatly, so if you have scraped lots of data (and have it on your local disk) you can test different chunking and indexing strategies.

Therefore a brain can be thought of a pipeline of a scraper > chunker > embedder > vector DB. The last 2 steps, embedding & adding to the vector DB are subsumized in the `indexing` step.

The `brain` class acts as a wrapper around 
* the Chroma DB
* the refreence to the emebedding model - that is part of the Chroma settings
* the local file storage in which the imported documents and chunks are stored.

It's relevant methods are
* `import_documents`
* `import_chunks`
* `search_chunks_by_text`


Those pipeline components need configuration to become executable. A Wikipedias scraper needs the starting page, the number of hops to scrape from that page etc. Configured instances of those components are built by the corresponding factories:
* the scraper factory
* the chunker factory
* the indexer factory
Typically factories get a `parameters` object that contains everything they need to know. As the search parameters match the index parameters to a large extend (namely you have to use the same way of calculating the embeddings), you can use the the parameter set of the indexer factory also for the brain factory.

A configured scraper knows when it was run the last time. 

Scrapers (planned and done):
* **Wikipedia** ✅: Given a start page on Wikipedia and a depth (i.e. how many links should the crawler go down), the wikipedia data is scraped and added to the brain.
* Confluence
* Email
* Discourse

## The Prompts

Prompt templates are strings with placeholders for variables. As a starting point I use a list of constants and the [Standard Python Format String Syntax](https://docs.python.org/3/library/string.html#format-string-syntax).

Example: 
```python
prompt_template = """
DOCUMENT:
{documents}

QUESTION:
{question}

INSTRUCTIONS:
Answer the users QUESTION using the DOCUMENT text above.
Keep your answer ground in the facts of the DOCUMENT.
If the DOCUMENT doesn’t contain the facts to answer the QUESTION return NONE.
"""
```
Prompt templates are identidied by an `ID`. The prompts library offers 2 key functions:

```python
def get_prompt_template(prompt_id: str) -> str:

def get_prompt(prompt_template_id:str, **kwargs) -> str:
```

The 2nd argument to the `get_prompt` function are the replacements for the placeholders in the prompt. 

```python
prompt_fields = {
  "documents": """
Marie Curie (1867–1934) was a Polish and naturalised-French physicist and chemist who conducted pioneering research on radioactivity. Born in Warsaw, she studied in Poland until she was 24, when she moved to Paris to earn her higher degrees.
  """,
  "question": "Was Marie-Curie french?"
}
```

## Use cases

Use cases one could think of:
 
* Manual of software package or library: Add all the manual documents to a brain and question it.
* IT Assiatnt: Load all the confluence space of an IT organisation and assist based on that knowledge.
* Better writing assistant: Maybe even integrated into a Confluence plugin.
* Update documentation: The AI could scan the git diffs from one version to another and suggest modifications of the documentation.

## Code hygiene

our code is formatted with [black](https://github.com/psf/black) and linted with [flake8](https://flake8.pycqa.org/en/latest/).

* flake8 is configured via [setup.cfg](setup.cfg)
* black is configured via the [pyproject.toml](pyproject.toml)

## TODO

* Add `mypy` typecheccking to tests and/or build
* Finish the migration to a proper `llm_wrapper` class and the `ollama_wrapper` subclass
* Create shell scripts to format and lint code.
* Introduce a build system that uses `pyproject.toml` properly.
* To make the terminal user friendly in the devcontainer setup read thru the article [VSCode devcontainer with zsh, oh-my-zsh and agnoster theme](https://medium.com/@jamiekt/vscode-devcontainer-with-zsh-oh-my-zsh-and-agnoster-theme-8adf884ad9f6)
* Annotate `@override` in ch~~ld brains and chains.
* Review if it still makes sense to keep the documents as files in brains.
* Add a brain scraper for Atlassian Confluences, and test / demo it with [my private demo space](https://ai-platform-2024.atlassian.net/wiki/home)
* Add a brain scraper for emails.
* Visualize the chunks in their original document. Use this? [How to highlight any web page on Google Chrome (or Chromium-based Edge)](https://medium.com/@Bartleby/how-to-highlight-any-web-page-on-google-chrome-or-chromium-based-edge-83035c41eeec)
* Add pre-commit hooks
* The brain should keep track in the `_index.json` if a document was indexed, as well as using which embedding model
* Have a user friendly way (markdown?) of documentation for every chain.
* Have chain-specific parameter management incl. user interface. A12 models?
* Check if we can re-use parts of [this RAG Stack](https://pub.towardsai.net/the-best-rag-stack-to-date-8dc035075e13).

## DONE

* 2024-10-15: Added ba
  lack for Python Code Formatting and Flake8 for linting
* ~~Make sure that everywhere we mesn the `brain_id` we also call it `brain_id`. In many places currentyl we call it `brain`.~~
* ~~BUG: Paths are mixed up. Make sure that we always use absolute paths and start by the project root directory.~~
* ~~Make sure that all the APIs to the brain use the `brain_id`~~
* ~~Change brain management to a pipeline concept: Different stages that can be combined (i.e. scraping, chunking, indexing)~~
* ~~Re-structure the `ai_commons` to proper class files (`Documents`, `Chunks`) and separate factories for better readabilty.~~
* ~~Add a function `brain.import_or_update()`~~
* ~~API rule: Every call should return a `ìnner_working` dictionary, For the ai_brain this could contain: Brain name, no of docs/chunks, search time, result size...~~
* ~~Calling `python -m ai_brain` or similar should start the fastAPI server~~
* ~~Make ability to load a brain with data, have it's configuration in a YAML file~~


## Resources

* [A12 Widgets showcase](https://www.mgm-tp.com/a12.htmlshowcase/#/widgets/layout/application-frame)
* [Material Icons](https://fonts.google.com/icons?icon.set=Material+Icons)
* [Persist your React State in the Browser - DEV](https://dev.to/ajejey/persist-your-react-state-in-the-browser-2bgm)
* Pamela Fox Pathon AI Scripts, including streaming: [python-openai-demos](https://github.com/pamelafox/python-openai-demos)
* Pre-commit hooks: the [original documentation](https://pre-commit.com) 
* [Retrieval-Augmented Generation (RAG) from basics to advanced - Medium](https://medium.com/@tejpal.abhyuday/retrieval-augmented-generation-rag-from-basics-to-advanced-a2b068fd576c)
* [Advanced RAG 01: Small-to-Big Retrieval - Medium](https://towardsdatascience.com/advanced-rag-01-small-to-big-retrieval-172181b396d4)
* [Pydantic: Simplifying Data Validation in Python - Real Python](https://realpython.com/python-pydantic/)
* [Using FastAPI to Build Python Web APIs - Real Python](https://realpython.com/fastapi-python-web-apis/)
* [Embeddings and Vector Databases With ChromaDB - Real Python](https://realpython.com/chromadb-vector-database/)
* Original inspiration taken from [RAG on PostgreSQL - Github](https://github.com/Azure-Samples/rag-postgres-openai-python#) as explained in this video: [Building a RAG-powered AI chat app with Python and VS Code](https://www.youtube.com/watch?v=3ctFWU492xk&t=1177s)
* [Vector Admin - Github](https://github.com/Mintplex-Labs/vector-admin) a UI for vector databases
* [Microsoft Autogen - Github](https://github.com/microsoft/autogen), an open-source programming framework for building AI agents and facilitating cooperation among multiple agents to solve tasks.
* A command line tool for using AI assistants with a nice prompt management: [fabric](https://github.com/danielmiessler/fabric)

## Things to look at

* [10 essential tips to supercharge VS Code and code faster (0 to 100) - Medium](https://medium.com/coding-beauty/vscode-upgrade-tips-246481c27e8e)
* Intersting Prompts: [Apple Just Quietly Exposed The *AI Prompts* Powering Apple Intelligence](https://medium.com/macoclock/apple-just-quietly-exposed-the-ai-prompts-powering-apple-intelligence-b4ac3314eb14)
* A very nice overview on how to move on: [17 (Advanced) RAG Techniques to Turn Your LLM App Prototype into a Production-Ready Solution - Medium](https://towardsdatascience.com/17-advanced-rag-techniques-to-turn-your-rag-app-prototype-into-a-production-ready-solution-5a048e36cdc8)
* [Perplexica](https://github.com/ItzCrazyKns/Perplexica): Perplexica is an open-source AI-powered searching tool or an AI-powered search engine that goes deep into the internet to find answers.
* [Cursor](/https://www.cursor.com/features) Build software faster. Cursor includes a powerful autocomplete that predicts your next edit. Once enabled, it is always on and will suggest edits to your code across multiple lines, taking into account your recent changes.
