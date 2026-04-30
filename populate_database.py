import argparse
import os
import shutil
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from get_embedding_function import get_embedding_function
from langchain_chroma import Chroma


CHROMA_PATH = "chroma"
DATA_PATH = "data"


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    if args.reset:
        print("Clearing Database")
        clear_database()

    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)


def load_documents():
    document_loader = PyPDFDirectoryLoader(DATA_PATH)
    return document_loader.load()


def split_documents(documents: list[Document]):
    chunks = []
    
    for doc in documents:
        content = doc.page_content
        # Split by bullet points () which indicate new Q&A pairs
        qa_pairs = content.split('')
        
        for qa_pair in qa_pairs:
            qa_pair = qa_pair.strip()
            if qa_pair:
                # Try to separate question and answer more cleanly
                lines = qa_pair.split('\n')
                question = ""
                answer = ""
                
                # Find the question (line ending with ?)
                for i, line in enumerate(lines):
                    line = line.strip()
                    if line.endswith('?'):
                        question = line
                        # Everything after the question is the answer
                        answer = '\n'.join(lines[i+1:]).strip()
                        break
                
                if question and answer:
                    # Create a clean Q&A chunk
                    chunk = Document(
                        page_content=f"Question: {question}\nAnswer: {answer}",
                        metadata=doc.metadata
                    )
                    chunks.append(chunk)
                elif qa_pair:
                    # Fallback for any remaining content
                    chunk = Document(
                        page_content=qa_pair,
                        metadata=doc.metadata
                    )
                    chunks.append(chunk)
    
    return chunks


def add_to_chroma(chunks: list[Document]):
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
    )

    chunks_with_ids = calculate_chunk_ids(chunks)

    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
    else:
        print("No new documents to add")


def calculate_chunk_ids(chunks):


    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        chunk.metadata["id"] = chunk_id

    return chunks


def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)


if __name__ == "__main__":
    main()
