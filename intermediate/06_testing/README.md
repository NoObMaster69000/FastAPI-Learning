# Testing FastAPI Applications

This example demonstrates how to test a FastAPI application using `pytest` and `TestClient`.

## How to Run the Tests

The tests for this example are designed to be run from within this directory.

### 1. Install Dependencies

First, install the necessary Python packages. This includes `fastapi` itself, `uvicorn` to run the server, and the testing libraries `pytest`, `requests`, and `httpx`.

```bash
# Make sure you are inside the intermediate/06_testing directory
pip install -r requirements.txt
```

### 2. Run Pytest

Once the dependencies are installed, you can run the tests using `pytest`.

```bash
# Make sure you are inside the intermediate/06_testing directory
pytest
```

Pytest will automatically discover and run the tests in the `test_main.py` file. The tests are written to be independent and will pass when run in this self-contained environment.
