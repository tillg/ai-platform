# ai-platform

An AI Platform that consist of basic, functional modules.

![Overview](ai_platform_overview.svg)


## Local Development

### Setting up the environment 

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

### Running the components

Run the components:

```
# Orchestration
cd src
#python -m uvicorn ai_orchestration.main:app --reload
python -m ai_orchestration.main  

# AI Workspace
python -m ai_workspace.main
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

* Get type safety with pydantic - see [here](https://realpython.com/python-pydantic/#working-with-validators)

## Resources

* [Pydantic: Simplifying Data Validation in Python - Real Python](https://realpython.com/python-pydantic/)
* [Using FastAPI to Build Python Web APIs - Real Python](https://realpython.com/fastapi-python-web-apis/)
* [Embeddings and Vector Databases With ChromaDB - Real Python](https://realpython.com/chromadb-vector-database/)