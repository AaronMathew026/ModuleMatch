import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import tqdm
load_dotenv(override=True)
MODEL = "gpt-4-turbo"
client = OpenAI()
SYSTEM_PROMPT = '''You are a curriculum expert tasked with creating ultra-concise, 
keyword-focused summaries of university computer science modules.

Your constraints:
1. EXACTLY 2 sentences (not 2–3, not 1, not 3)
2. MAXIMUM 50 words total
3. NO redundancy (never repeat concepts)
4. PRIORITIZE technical keywords over explanation
5. Make every word count
6. Add unit code to very beginning of file

Technique: Lead with 1–2 core concepts. Follow with applications/outcomes.

Example Input:
"Focus on mathematical and applied logic: propositional logic, 
satisfiability-checking algorithms (DPLL, tableaux, randomized 
algorithms), and encoding problems into propositional formulas. 
Quantified Boolean Logic (QBF) and reasoning algorithms. Linear 
Temporal Logic (LTL): syntax, semantics, evaluation, equivalence. 
Model checking and verification algorithms for state-transition 
systems. OBDDs: structure, construction, combination. Applications 
to hardware/software verification."

Example Output:
"Master formal logic (propositional, QBF, LTL) and verification 
algorithms (DPLL, tableaux, OBDDs). Encode constraint-satisfaction 
systems, apply model-checking for hardware/software verification, 
and construct symbolic reasoning structures.'''

def main(File):
    print("Starting summarizer...")
    df = pd.read_csv(File)

    for index, row in tqdm.tqdm(df.iterrows()):
        description = row['description']
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": description}
            ],
            temperature=0.3,
            max_tokens=100
        )
        summary = response.choices[0].message.content
        df.at[index, 'summary'] = summary
        df.to_csv(File, index=False)  # Save after each update to prevent data loss



    print(df.head())
    print(df.at[0, 'summary'])

    


if __name__ == "__main__":
    main("raw_csv_data/modules.csv")



