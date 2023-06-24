import os
import pickle
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

def load_api_key():
    load_dotenv()  # Load environment variables from .env file
    return os.getenv("OPENAI_API_KEY")

def get_pdf_text(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as f:
        pdf_reader = PdfReader(f)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    openai_api_key = load_api_key()
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def main():
    pdf_path = "/home/alen/Desktop/llm_model/notification_data/notification.pdf"
    vectorstore_path = "/home/alen/Desktop/mini_project_19-06-23/processed_data/vectorstore.pkl"

    raw_text = get_pdf_text(pdf_path)
    text_chunks = get_text_chunks(raw_text)
    vectorstore = get_vectorstore(text_chunks)

    with open(vectorstore_path, "wb") as f:
        pickle.dump(vectorstore, f)

if __name__ == '__main__':
    main()
