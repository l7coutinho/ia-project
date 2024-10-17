import bs4

from dotenv import load_dotenv

from langchain_community.document_loaders import WebBaseLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()

def get_retriever(url):
    loader = WebBaseLoader(
        web_paths=(url,),
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
    return retriever
