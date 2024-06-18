# ai-platform

An AI Platform that consist of basic, functional modules.


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

### Running the frontend and backend

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

## Resources

* [Using FastAPI to Build Python Web APIs - Real Python](https://realpython.com/fastapi-python-web-apis/)