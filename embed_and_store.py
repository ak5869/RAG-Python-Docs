# embed_and_store.py
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma

# Load the content
with open("python_docs.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

# Chunk it
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.create_documents([raw_text])

# Embed
embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# Store in ChromaDB
db = Chroma.from_documents(docs, embedding, persist_directory="./chroma_db")
db.persist()
