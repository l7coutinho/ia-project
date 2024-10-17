from fastapi import FastAPI
from langchain import hub
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langserve import add_routes
from dotenv import load_dotenv
import bs4
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
)

llm = ChatGroq(model="llama3-8b-8192")

loader = WebBaseLoader(
    web_paths=("https://pt.wikipedia.org/wiki/Neymar",),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("mw-body-content")
        )
    ),
)
docs = loader.load()
print(f"Loaded {len(docs)} documents")

if not docs:
    raise ValueError("No documents were loaded. Check the URL and parsing settings.")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
print(f"Created {len(splits)} splits")

if not splits:
    raise ValueError("No splits were created. Check the text splitter settings.")

vectorstore = Chroma.from_documents(
    documents=splits, 
    embedding=OpenAIEmbeddings(),
    persist_directory="./chroma_db"
)
print("Vectorstore created successfully")

retriever = vectorstore.as_retriever()
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