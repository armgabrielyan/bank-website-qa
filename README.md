# Bank website chatbot

## Setup

1. Install Tesseract by the following [instructions](https://tesseract-ocr.github.io/tessdoc/Installation.html).

2. Create a Python virtual environment.

```shell
python3.12 -m venv .venv
```

3. Activate the virtual environment.

```shell
source .venv/bin/activate
```

4. Install Python dependency packages.

```shell
pip install -r requirements.txt
```

## Prerequisites

1. Create a `.env` file.

```shell
cp .env.example .env
```

#### LLM providers

- [Groq](https://groq.com/)

Create an API key at [Groq developer console](https://console.groq.com/keys). Free tier should be sufficient.

By default, `llama-3.3-70b-versatile` model is used, but other models can be used [supported by Groq](https://console.groq.com/docs/models).

## Data preparation

1. Extract texts from screenshots of web pages.

```shell
python -m scripts.extractor
```

2. Ingest text documents into vector db.

```shell
python -m scripts.ingestor
```

## Run

### API

```shell
python -m app.main
```

Visit [Swagger docs](http://localhost:8080/docs) for documentation and trying it out.

### Streamlit app

```shell
streamlit run streamlit_demo.py
```
