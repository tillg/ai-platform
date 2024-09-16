# ai-platform 🧠

An AI Platform that consist of basic, functional modules and that is prepared to tinker with it.

![Overview](ai_platform_overview.svg)


## Local Development

### Setting up & running

In order to install the server side:
* Make sure you are in the root directory of the project
* Create a local Python env: `python3.12 -m venv .venv`
* Activate it: `source .venv/bin/activate`
* Install the requirements: `pip install -r requirements.txt`

For the frontend:
```
cd src/ai_ui
npm install
```

Run the backend components:

```
# Orchestration
cd src
python -m ai_orchestration.main  

# AI Workspace
python -m ai_workspace.main
```

To start all the backend components at one there is a script:
```bash
cd src
./start_backend.sh
```

Run the AI-UI: 
```bash
cd src/ai_ui
npm run dev
```

Run the A12 based UI:
```bash
cd src/ai_ui_a12
npm start
```
Run tests:
* Make sure you are in the `src` directory
* `python -m pytest backend_tests --capture=no --log-cli-level=INFO`
  * Note: This is to also see the print and log statements.

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

## The UI

The UI is inspired from [RAG on PostgreSQL - Github](https://github.com/Azure-Samples/rag-postgres-openai-python#) as explained in this video: [Building a RAG-powered AI chat app with Python and VS Code](https://www.youtube.com/watch?v=3ctFWU492xk&t=1177s).

An impression of what it looks like:

![UI from rag OpenAI](image.png)

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

## Todo

* Re-structure the `ai_commons` to proper class files (`Documents`, `Chunks`) and separate factories for better readabilty.
* Add a brain scraper for Atlassian Confluences, and test / demo it with [my private demo space](https://ai-platform-2024.atlassian.net/wiki/home)
* Visualize the chunks in their original document. Use this? [How to highlight any web page on Google Chrome (or Chromium-based Edge)](https://medium.com/@Bartleby/how-to-highlight-any-web-page-on-google-chrome-or-chromium-based-edge-83035c41eeec)
* Add pre-commit hooks
* The brain should keep track in the `_index.json` if a document was indexed, as well as using which embedding model
* Add a function `brain.import_or_update()` 
* Data Loader for confluence pages and Emails
* ~~API rule: Every call should return a `ìnner_working` dictionary, For the ai_brain this could contain: Brain name, no of docs/chunks, search time, result size...~~
* ~~Calling `python -m ai_brain` or similar should start the fastAPI server~~
* Make ability to load a brain with data, have it's configuration in a YAML file
* Have a user friendly way (markdown?) of documentation for every chain.
* Have chain-specific parameter management incl. user interface. A12 models?
* Change brain management to a pipeline concept: Different stages that can be combined (i.e. scraping, chunking, indexing)

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

## Things to look at

* [10 essential tips to supercharge VS Code and code faster (0 to 100) - Medium](https://medium.com/coding-beauty/vscode-upgrade-tips-246481c27e8e)
* Intersting Prompts: [Apple Just Quietly Exposed The *AI Prompts* Powering Apple Intelligence](https://medium.com/macoclock/apple-just-quietly-exposed-the-ai-prompts-powering-apple-intelligence-b4ac3314eb14)
* A very nice overview on how to move on: [17 (Advanced) RAG Techniques to Turn Your LLM App Prototype into a Production-Ready Solution - Medium](https://towardsdatascience.com/17-advanced-rag-techniques-to-turn-your-rag-app-prototype-into-a-production-ready-solution-5a048e36cdc8)
* [Perplexica](https://github.com/ItzCrazyKns/Perplexica): Perplexica is an open-source AI-powered searching tool or an AI-powered search engine that goes deep into the internet to find answers.
* [Cursor](/https://www.cursor.com/features) Build software faster. Cursor includes a powerful autocomplete that predicts your next edit. Once enabled, it is always on and will suggest edits to your code across multiple lines, taking into account your recent changes.
