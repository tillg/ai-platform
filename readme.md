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

A brain is a Vectore Database (or a namespace within a vector DB) that contains documents / embeddings about a certain domain. It is typically attached to a loader that configures what data is to be loaded from where.

Technically the Brain contains 2 data storages and one index file:

* `documents`: This is a directory with json files, one for each document.
* `chroma`: This is a directory that contains the ChromaDB with the indexes of the chunks.
* `_index.json` contains a list of all the files in `documents` with some meta data - most notably the URI pointing to the initial location of that document.

Filling a brain with consists of the following steps:

* `acquisition` imports the documents. THis is typically done by a scraping process. We provide different `data_acquirer`
* Indexing, that comprises
  * `chunk` cuts the documents in chunks
  * `index` imports the chunks with their embedding as index

These indexing steps  are performed by the `brain` itself.

A brain is typically attached to a loader - the software that ingests the data into the brain.

Loaders (planned and done):
* **Wikipedia** ✅: Given a start page on Wikipedia and a depth (i.e. how many links should the crawler go down), the wikipedia data is scraped and added to the brain.
* Confluence
* Email
* Discourse


**Notes**
* The Loader config is specific to the different loaders we have
* The `NoOfDocs` and `NoOfChunks` values are updated every time the brain info is questioned.

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

* Visualize the chunks in their original document. Use this? [How to highlight any web page on Google Chrome (or Chromium-based Edge)](https://medium.com/@Bartleby/how-to-highlight-any-web-page-on-google-chrome-or-chromium-based-edge-83035c41eeec)
* Add pre-commit hooks
* The brain should keep track in the `_index.json` if a document was indexed, as well as using which embedding model
* Add a function `brain.import_or_update()` 
* Data Loader for confluence pages and Emails
* API rule: Every call should return a `ìnner_working` dictionary, For the ai_brain this could contain: Brain name, no of docs/chunks, search time, result size...
* Calling `python -m ai_brain` or similar should start the fastAPI server
* Make ability to load a brain with data, have it's configuration in a YAML file

## Resources

* Intersting Prompts: [Apple Just Quietly Exposed The *AI Prompts* Powering Apple Intelligence](https://medium.com/macoclock/apple-just-quietly-exposed-the-ai-prompts-powering-apple-intelligence-b4ac3314eb14)
* Pamela Fox Pathon AI Scripts, including streaming: [python-openai-demos](https://github.com/pamelafox/python-openai-demos)
* Pre-commit hooks: the [original documentation](https://pre-commit.com) 
* [A12 Widgets showcase](https://www.mgm-tp.com/a12.htmlshowcase/#/widgets/layout/application-frame)
* A very nice overview on how to move on: [17 (Advanced) RAG Techniques to Turn Your LLM App Prototype into a Production-Ready Solution - Medium](https://towardsdatascience.com/17-advanced-rag-techniques-to-turn-your-rag-app-prototype-into-a-production-ready-solution-5a048e36cdc8)
* [Retrieval-Augmented Generation (RAG) from basics to advanced - Medium](https://medium.com/@tejpal.abhyuday/retrieval-augmented-generation-rag-from-basics-to-advanced-a2b068fd576c)
* [Advanced RAG 01: Small-to-Big Retrieval - Medium](https://towardsdatascience.com/advanced-rag-01-small-to-big-retrieval-172181b396d4)
* [Pydantic: Simplifying Data Validation in Python - Real Python](https://realpython.com/python-pydantic/)
* [Using FastAPI to Build Python Web APIs - Real Python](https://realpython.com/fastapi-python-web-apis/)
* [Embeddings and Vector Databases With ChromaDB - Real Python](https://realpython.com/chromadb-vector-database/)
* Original inspiration taken from [RAG on PostgreSQL - Github](https://github.com/Azure-Samples/rag-postgres-openai-python#) as explained in this video: [Building a RAG-powered AI chat app with Python and VS Code](https://www.youtube.com/watch?v=3ctFWU492xk&t=1177s)


### Things to look at 

apple-just-quietly-exposed-the-ai-prompts-powering-apple-intelligence-b4ac3314eb14)
* https://medium.com/coding-beauty/vscode-upgrade-tips-246481c27e8e