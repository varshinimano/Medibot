from src.helper import (
    load_pdf_file,
    text_split,
    download_huggingface_embeddings
)

from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv

import os
import time


# Load environment variables
load_dotenv()

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY is not set.")


# Connect to Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)


# Pinecone index name
index_name = "medibot"

# all-MiniLM-L6-v2 produces 384-dimensional embeddings
embedding_dimension = 384


# Check whether the index already exists
existing_indexes = pc.list_indexes().names()


if index_name not in existing_indexes:

    print("Pinecone index does not exist.")
    print("Creating 384-dimensional Pinecone index...")

    pc.create_index(
        name=index_name,
        dimension=embedding_dimension,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

    print("Pinecone index created.")

    # Wait until the index is ready
    while True:
        index_info = pc.describe_index(index_name)

        if index_info.status["ready"]:
            break

        print("Waiting for Pinecone index to become ready...")
        time.sleep(2)

else:

    print("Pinecone index already exists.")

    # Verify the index dimension
    index_info = pc.describe_index(index_name)

    current_dimension = index_info.dimension

    print("Pinecone index dimension:", current_dimension)

    if current_dimension != embedding_dimension:

        raise ValueError(
            f"Pinecone index dimension is {current_dimension}, "
            f"but Hugging Face embeddings require "
            f"{embedding_dimension} dimensions."
        )


# Load PDF files
print("Loading PDF files...")

extracted_data = load_pdf_file(data="Data/")

print("PDF files loaded:", len(extracted_data))


# Split PDF into chunks
print("Splitting documents...")

text_chunks = text_split(extracted_data)

print("Number of text chunks:", len(text_chunks))


# Load Hugging Face embeddings
print("Loading Hugging Face embedding model...")

embeddings = download_huggingface_embeddings()

print("Embedding model loaded.")


# Store documents and embeddings in Pinecone
print("Storing documents in Pinecone...")

docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings
)


print("Documents successfully stored in Pinecone.")
print("Indexing completed successfully.")