# MLE Agent

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)

A Machine Learning Engineer Agent using LangGraph and Gemini (Google Generative AI).

## Features
- Conversational AI using Gemini via Google API
- Modular graph-based workflow with LangGraph
- Environment variable management with `.env`
- Pythonic, extensible codebase

## Requirements
- Python 3.12 (see `.python-version`)
- See `pyproject.toml` for dependencies

## Setup
1. Clone the repository
2. Create a virtual environment (recommended):
   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   # or, if using poetry or uv:
   poetry install
   # or
   uv pip install -r requirements.txt
   ```
4. Add your Google API key to a `.env` file:
   ```
   GOOGLE_API_KEY=your-key-here
   ```

## Usage
Run the main script:
```bash
python main.py
```

## Python Version
This project uses **Python 3.12**

## License
[MIT](LICENSE)
