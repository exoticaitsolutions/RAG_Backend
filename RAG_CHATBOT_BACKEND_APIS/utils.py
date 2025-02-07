import logging
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma


# Create a logger instance
logger = logging.getLogger(__name__)

# Global variable declaration


def save_pdf_to_chroma(pdf_file_path):
    """Extract text from PDF and save it to Chroma DB."""
    try:
        loader = PyPDFLoader(pdf_file_path)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)
        embeddings = OpenAIEmbeddings()
       
        vectordb = Chroma.from_documents(texts, embeddings, persist_directory="chroma_db")
        vectordb.get()

  
        return "PDF processed and stored in ChromaDB."
    except Exception as e:
        logger.error(f"Error processing PDF {pdf_file_path}: {e}")
        return str(e)



def query_chroma(query_text):
    """Queries ChromaDB and retrieves results."""
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory="chroma_db", embedding_function=embeddings)
    results = vectordb.similarity_search(query_text, k=5)
    if results:
        return  [{'text': res.page_content, 'reference': res.metadata.get('source', 'Unknown')} for res in results]
    else:
        vectordb.add_documents([query_text])
        vectordb.persist()
        return 'No matching results. Query stored for future reference.'

