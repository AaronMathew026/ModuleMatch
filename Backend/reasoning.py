import os
import os
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from openai import OpenAI


load_dotenv(override=True)
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

db_name = "Backend/Embeddings/module_embeddings.db"

def main(mode,input=None):
    if mode == "embedding":
        print("Creating Embeddings...")
        embedding("Backend/raw_csv_data/CS_Modules.csv",)
    elif mode == "semantic_search":
        print("Semantic Search")
        semantic_search(input)
    elif mode == "reasoning":
        print("Reasoning")
        llm_ranker()
        pass

def embedding(file, test=False):
    df = pd.read_csv(file)
    documents = []
    
    for index, course in tqdm(df.iterrows(), total=len(df), desc="Creating Documents"):
        doc = Document(
            page_content=course["summary"],
            metadata={
                "code": course["code"],
                "title": course["title"],
                "year": course["year"],
            },
        )
        doc.metadata["doc_type"] = "course"
        documents.append(doc)
        
    print(f"Created {len(documents)} documents for embedding.")
    
    if os.path.exists(db_name):
        Chroma(persist_directory=db_name, embedding_function=embeddings).delete_collection()
        
    vectorstore = Chroma.from_documents(documents, embeddings, persist_directory=db_name)

    if test:

        collection = vectorstore._collection
        count = collection.count()

        sample_embedding = collection.get(limit=1, include=["embeddings"])["embeddings"][0]
        dimensions = len(sample_embedding)
        print(f"There are {count:,} vectors with {dimensions:,} dimensions in the vector store")

def semantic_search(string):
    print("Performing Semantic Search...")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    vectorstore = Chroma(persist_directory=db_name, embedding_function=embeddings)
    retriever = vectorstore.as_retriever()
    results = retriever.invoke(string)
    print("Semantic Search Complete...")
    return results


def llm_ranker(CV, goals_interests):
    print("Ranking Courses with LLM...")
    documents = semantic_search(CV)
    client = OpenAI()
    USERPROMPT = f"""
You are a university module recommendation expert.
Given a student's CV and top 10 semantically similar courses,
rank them by career fit and explain each ranking.

CV Summary: {CV}
goals and interests: {goals_interests}

Top 10 Courses:
{documents}

Rank these courses 1–10. For each, explain:
1. Why it matches the CV
2. Career value
3. Difficulty fit
Format: JSON with ranking array
"""
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": USERPROMPT}],
        reasoning_effort="medium",
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content



if __name__ == "__main__":

    main("reasoning")
    