import os
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from openai import OpenAI

# Load environment variables (ensure OPENAI_API_KEY is set in your .env)
load_dotenv(override=True)
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# FIX: Dynamic absolute path mapping so FastAPI can always find the DB
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_name = os.path.join(BASE_DIR, "Embeddings", "module_embeddings.db")

def main(data):
    llm_response = llm_ranker(data)
    return llm_response

def embedding(file, test=True):
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
    
    # Clear out the old database
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
    print(f"Searching for: {string}")
    
    # Initialize the vector store connection
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    vectorstore = Chroma(persist_directory=db_name, embedding_function=embeddings)
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
    results = retriever.invoke(string)
    
    print("Semantic Search Complete...")
    print(f"Found {len(results)} results.")
    return results

def cv_summary(cv_text, goals):
    print("Summarizing CV with LLM...")
    client = OpenAI()
    USER_PROMPT = f"""
You are a concise résumé summariser. Produce a short, keyword-rich profile summary from a student's CV. Output exactly three parts in plain text separated by blank lines:
1) One-line career goal (<=15 words).
2) Two to three concise sentences (<=50 words) describing core skills, domain experience, and tools.
3) A comma-separated bullet list labeled "SKILLS:" containing 6–12 keywords (languages, frameworks, algorithms, topics).

Do not invent facts. If CV lacks a field, omit it. Prioritise technical keywords and outcomes.

CV_TEXT:
{cv_text}

Goals: {goals}

Instruction: Produce the three-part summary described above. Focus on technical skills and stated goals. Return only the three parts, with exactly one blank line between parts.
"""

    response = client.chat.completions.create(
        model="o3-mini", 
        messages=[{"role": "user", "content": USER_PROMPT}],
        reasoning_effort="medium",
    )
    
    response_text = response.choices[0].message.content
    print("CV Summary Complete...")
    print(f"Summary:\n{response_text}\n")
    
    return response_text

def llm_ranker(data):
    print("Ranking Courses with LLM...")
    print(f"Data received for ranking: {data}")
    
    # 1. Summarize the CV
    cv_summary_text = cv_summary(data["cv_text"], data["goals"])
    print(f"CV Summary Text:\n{cv_summary_text}\n")

    # 2. Fetch the top 10 documents
    documents = semantic_search(cv_summary_text)
    

    formatted_courses = ""
    for i, doc in enumerate(documents, 1):
        formatted_courses += f"{i}. Code: {doc.metadata.get('code')} | Title: {doc.metadata.get('title')}\n"
        formatted_courses += f"   Summary: {doc.page_content}\n\n"

    client = OpenAI()
    USERPROMPT = f"""
You are a university module recommendation expert.
Given a student's CV and top 10 semantically similar courses, rank them by career fit and explain each ranking.

UserInfo: {data["student_name"]}, Year {data["year"]}, Course: {data["course"]}
CV Summary: {cv_summary_text}
Goals and interests: {data["goals"]}, {data["interests"]}

Top Courses:
{formatted_courses}

Rank these courses 1-10. For each, explain:
1. Why it matches the CV
2. Career value
3. Difficulty fit

Format: MarkDown list with course code, title, and explanation.
"""
    
    response = client.chat.completions.create(
        model="o3-mini",
        messages=[{"role": "user", "content": USERPROMPT}],
        reasoning_effort="medium",
    )
    
    final_output = response.choices[0].message.content
    print(final_output)
    
    return final_output


# data = {
#     "student_name": "Alice",
#     "year": 2,
#     "course": "Computer Science",
#     "cv_text": """Aspiring AI Engineer focused on building autonomous, data-driven intelligent systems.

# Proficient in Python with extensive project experience in autonomous AI, NLP, and real-time applications. Developed production-grade systems using Django, FastAPI, and web technologies while integrating REST APIs, cron scheduling, and data pipelines.

# SKILLS: Python, AI Engineering, Machine Learning, NLP, Django, FastAPI, PostgreSQL, WebRTC, Pandas, Docker, Git, Linux""",
#     "goals": "Alice wants to specialize in AI and work in the tech industry after graduation.",
#     "interests": "Alice is interested in machine learning, data science, and software engineering."
# }
# llm_ranker(data)