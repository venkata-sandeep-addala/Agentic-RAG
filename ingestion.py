from dotenv import load_dotenv

load_dotenv()

from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

URLs = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]


docs = WebBaseLoader(web_paths=URLs).load()

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=250, chunk_overlap=0
)

chunks = text_splitter.split_documents(docs)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# vector_store = Chroma.from_documents(documents=chunks,
#                            embedding=embeddings,
#                            collection_name="rag-chroma",
#                            persist_directory="./.chroma")


retriever = Chroma(
    collection_name="rag-chroma", persist_directory="./.chroma", embedding_function=embeddings
).as_retriever()
