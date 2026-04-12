import pandas as pd
from tqdm import tqdm
from openai import OpenAI
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
import os
load_dotenv(override=True)
embeddings = OpenAIEmbeddings(model="text-embedding-3-large", client=OpenAI())

db_name = f"Backend\\Embeddings\\module_embeddings.db"

def main():
    embedding("Backend\\raw_csv_data\\CS_Modules.csv",)
    


    pass





def embedding(file,):
    documents = []
    df = pd.read_csv(file)
    documents = [
    {
        "metadata": {
            "code": course["code"],
            "title": course["title"],
            "year": course["year"]
        },
        "page_content": course["summary"]
    }
    for index,course in df.iterrows()
    ]
    print(f"Created {len(documents)} documents for embedding.")
    if os.path.exists(db_name):
        os.remove(db_name)


if __name__ == "__main__":
    main()




