from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain_core.runnables import Runnable
from langchain.chains import RetrievalQA
import requests


embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma(persist_directory="./chroma_db", embedding_function=embedding)

llm = Ollama(model="mistral")
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever())

# Sample query
query = "How do I define a function in Python?"
response = qa_chain.run(query)
print(response)
