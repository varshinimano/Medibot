# Medical Chatbot

A **RAG-based Medical Chatbot** that answers questions using information from medical PDF documents.

## Features

* Load medical information from PDF files
* Split documents into text chunks
* Generate embeddings using OpenAI
* Store and search embeddings using Pinecone
* Retrieve relevant information for user questions
* Generate answers using OpenAI
* Simple Flask web interface

## Technologies

* Python
* Flask
* LangChain
* OpenAI
* Pinecone
* HTML, CSS, JavaScript

## Project Structure

```text
Medical_Chatbot/
│
├── Data/
├── src/
│   ├── __init__.py
│   ├── helper.py
│   └── prompt.py
│
├── templates/
│   └── chat.html
│
├── app.py
├── store_index.py
├── requirements.txt
├── setup.py
├── test.py
├── .env
├── .gitignore
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd Medical_Chatbot
```

### 2. Create and activate the environment

```bash
conda create -n medical python=3.10
conda activate medical
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```text
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
```

Do not upload the `.env` file to GitHub.

## Pinecone Setup

Create a Pinecone index named:

```text
medibot
```

The index should use:

```text
Dimension: 512
Metric: cosine
```

## Index the Documents

Place the medical PDF files inside the `Data/` folder.

Then run:

```bash
python store_index.py
```

This loads the PDFs, creates text chunks, generates embeddings, and stores them in Pinecone.

## Run the Application

After indexing the documents:

```bash
python app.py
```

Open:

```text
http://localhost:8080
```

and start asking questions.

## Note

This chatbot is intended for educational purposes and should not be used as a substitute for professional medical advice.

314068109147.dkr.ecr.us-east-1.amazonaws.com/medibot