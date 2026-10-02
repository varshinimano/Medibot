from flask import Flask, render_template, request

from src.helper import download_huggingface_embeddings
from src.prompt import system_prompt

from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv

import os


app = Flask(__name__)

load_dotenv()


# Load environment variables
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY is not set.")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set.")


# Set API keys
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


# Load Hugging Face embeddings
embeddings = download_huggingface_embeddings()


# Pinecone index
index_name = "medibot"


# Connect to existing Pinecone index
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)


# Create retriever
retriever = docsearch.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)


# Format retrieved documents into plain text
def format_docs(docs):
    return "\n\n".join(
        document.page_content
        for document in docs
    )


# OpenAI is used only as the chat/generation model
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    max_tokens=300
)


# Prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}")
    ]
)


# RAG chain
rag_chain = (
    {
        "context": retriever | format_docs,
        "input": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)


@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/get", methods=["GET", "POST"])
def chat():

    msg = request.form["msg"]

    print("Question:", msg)

    response = rag_chain.invoke(msg)

    print("Response:", response)

    return str(response)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=False
    )