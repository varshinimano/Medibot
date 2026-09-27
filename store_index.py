from src.helper import load_pdf_file, text_split, download_openai_embeddings

from pinecone import Pinecone

from langchain_pinecone import PineconeVectorStore

from dotenv import load_dotenv

import os


# Load environment variables
load_dotenv()

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY


# Load PDF files
extracted_data = load_pdf_file(data="Data/")


# Split PDF into chunks
text_chunks = text_split(extracted_data)


# Load OpenAI embedding model
embeddings = download_openai_embeddings()


# Connect to Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)


# Existing Pinecone index
index_name = "medibot"


# Store document chunks and embeddings in Pinecone
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings
)