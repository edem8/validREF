from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS

def get_vector_store(chunks):
    embeddings = HuggingFaceInstructEmbeddings(model_name='hkunlp/instructor-xl')
    vectorstore =  FAISS.from_texts(texts=chunks, embeddings=embeddings)

    return vectorstore