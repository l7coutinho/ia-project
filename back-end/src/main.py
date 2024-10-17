from langchain import hub
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from vectordb import get_retriever

load_dotenv()

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
)

llm = ChatGroq(model="llama3-8b-8192")

retriever = get_retriever("https://pt.wikipedia.org/wiki/Neymar")
prompt = hub.pull("rlm/rag-prompt")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_routes(
    app,
    rag_chain,
    path="/rag",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)