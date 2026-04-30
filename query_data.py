import os
import argparse
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

from get_embedding_function import get_embedding_function

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
You are a NUST(university) assistant. Look at the user question and the context below.

Context:
{context}

User Question: {question}

Instructions:
1. There are many questions with their answers in the context above.
2. If the user question is similar to any of the questions in the context or if you think the user is asking something that is already asked in one of the FAQs, provide the corresponding answer.
3. Don't overthink and don't add any extra information.
4. Don't hallucinate and don't make up answers.
5. If there is some link in the answer then that link is the valid answer, give exact clickable link in answer.
6. If no match, respond with: out of scope.
7. But please don't respond with out of scope on questions that have answers in the context

Answer:
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)


def query_rag(query_text: str, db_path: str):
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=db_path, embedding_function=embedding_function)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in db.similarity_search_with_score(query_text, k=3)])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    import re
    def remove_think_blocks(text):
        return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)

    model = OllamaLLM(model="deepseek-r1:1.5b")
    response_text = model.invoke(prompt)
    response_text = remove_think_blocks(response_text)
    cleaned_response = re.sub(r"^\s*Answer:.*$", "", response_text, flags=re.MULTILINE).strip()
    
    print(cleaned_response)
    return cleaned_response


if __name__ == "__main__":
    main()
