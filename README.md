# Medical Chatbot

A **RAG-based Medical Chatbot** that answers questions using information from medical PDF documents.

## Features

* Load medical information from PDF files
* Split documents into text chunks
* Generate embeddings using Hugging Face `all-MiniLM-L6-v2`
* Store and search embeddings using Pinecone
* Retrieve relevant information for user questions
* Generate answers using OpenAI GPT-4o-mini
* Simple Flask web interface
* Containerized using Docker
* Deployed using Amazon ECR and Amazon EC2
* Automated CI/CD using GitHub Actions

## Technologies

* Python
* Flask
* LangChain
* Hugging Face
* Sentence Transformers
* Pinecone
* OpenAI
* Docker
* Amazon ECR
* Amazon EC2
* GitHub Actions
* HTML, CSS, JavaScript

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/varshinimano/Medibot.git

cd Medibot
```

### 2. Create and activate the environment

```bash
conda create -n medibot python=3.10

conda activate medibot
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

Use the following configuration:

```text
Dimension: 384
Metric: cosine
```

The project uses the Hugging Face model:

```text
sentence-transformers/all-MiniLM-L6-v2
```

## Index the Documents

Place the medical PDF files inside the `Data/` folder.

Then run:

```bash
python store_index.py
```

This loads the PDFs, creates text chunks, generates Hugging Face embeddings, and stores them in Pinecone.

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

## Docker

Build the Docker image:

```bash
docker build -t medibot .
```

Run the container:

```bash
docker run -p 8080:8080 --env-file .env medibot
```

Open:

```text
http://localhost:8080
```

## AWS Deployment

The application is containerized using Docker and deployed on AWS.

* Docker image is stored in **Amazon ECR**
* Application runs on **Amazon EC2**
* Port `8080` is exposed for the Flask application
* GitHub Actions is configured for CI/CD
* On every push to the `main` branch, GitHub Actions builds the Docker image and pushes it to Amazon ECR
* The EC2 self-hosted runner pulls the latest image and runs the updated container

## Project Structure

```text
Medibot/
│
├── Data/
├── src/
│   ├── helper.py
│   └── prompt.py
│
├── templates/
│   └── chat.html
│
├── .github/
│   └── workflows/
│       └── cicd.yaml
│
├── app.py
├── store_index.py
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── setup.py
└── README.md
```

## Note

This chatbot is intended for educational purposes and should not be used as a substitute for professional medical advice.
