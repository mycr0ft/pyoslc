# PyOSLC SDK

The `PyOSLC` project is a set of classes and libraries packaged as an SDK
for building REST-based APIs that implement
`OSLC (Open Services for Lifecycle Collaboration)` specifications,
enabling the interoperability of heterogeneous products and services.

## Requirements

- **Python >= 3.10**
- [uv](https://github.com/astral-sh/uv) (package manager)

## Getting Started

### Clone the repository

```bash
$ git clone git@github.com:cslab/pyoslc.git
$ cd pyoslc
```

### Set up the environment

```bash
$ uv venv
$ uv sync
```

For test dependencies:

```bash
$ uv sync --extra test
```

### Run the demo

```bash
$ flask run
```

Navigate to [http://127.0.0.1:5000/oslc](http://127.0.0.1:5000/oslc) to see the demo.

![PyOSLC Demo](docs/source/_static/02.png "PyOSLC Demo")

## Project Structure

```
pyoslc/
├── pyproject.toml        # Project metadata and dependencies
├── setup.py              # Backward-compat stub for pip install -e .
├── app/                  # Example Flask application
├── pyoslc/               # SDK: core classes for building OSLC APIs
├── pyoslc_oauth/         # OAuth 1.0a authentication & authorization
├── examples/             # Sample data for the demo
├── tests/                # Test suite (pytest)
└── docs/                 # Documentation (Sphinx)
```

## Running Tests

```bash
$ uv run pytest -v
```

## Linting

```bash
$ uv run flake8 pyoslc app pyoslc_oauth
```