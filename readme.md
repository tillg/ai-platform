# ai-platform 🧠

An AI Platform that consist of basic, functional modules.

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
#python -m uvicorn ai_orchestration.main:app --reload
python -m ai_orchestration.main  

# AI Workspace
python -m ai_workspace.main
```

Run the AI-UI: 
```bash
cd src/ai_ui
npm run dev
```

Run tests:
* Make sure you are in the `src` directory
* `python -m pytest backend_tests --capture=no --log-cli-level=INFO`
  * Note: This is to also see the print and log statements.

### Running the tests

```
cd src

# Run the tests of one compnenent, for example ai_commons
python -m unittest discover ai_commons_tests

# Run all the unit tests
python -m unittest discover . 
```

## Todo

* Calling `python -m ai_brain` or similar should start the fastAPI server
* Make ability to load a brain with data, have it's configuration in a YAML file

## Resources

* [Retrieval-Augmented Generation (RAG) from basics to advanced - Medium](https://medium.com/@tejpal.abhyuday/retrieval-augmented-generation-rag-from-basics-to-advanced-a2b068fd576c)
* [Advanced RAG 01: Small-to-Big Retrieval - Medium](https://towardsdatascience.com/advanced-rag-01-small-to-big-retrieval-172181b396d4)
* [Pydantic: Simplifying Data Validation in Python - Real Python](https://realpython.com/python-pydantic/)
* [Using FastAPI to Build Python Web APIs - Real Python](https://realpython.com/fastapi-python-web-apis/)
* [Embeddings and Vector Databases With ChromaDB - Real Python](https://realpython.com/chromadb-vector-database/)