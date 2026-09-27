from flask import Flask, render_template, request

from src.helper import download_openai_embeddings
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

PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')
OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

embeddings = download_openai_embeddings()


index_name = "medibot"

# Embed each chunk and upsert the embeddings into your Pinecone index.
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.4,
    max_tokens=500
)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}")
    ]
)

rag_chain = (
    {
        "context": retriever,
        "input": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)


@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]

    print("Question : ", msg)

    response = rag_chain.invoke(msg)

    print("Response : ", response)

    return str(response)




if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8080, debug= True)
