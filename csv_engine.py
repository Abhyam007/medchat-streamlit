import pandas as pd
from config import Config

df = pd.read_csv(Config.CSV_PATH)

def normalize(text):
    return str(text).lower().strip()

def search_csv(query):
    q = normalize(query)

    # Exact + partial match
    for _, row in df.iterrows():
        question = normalize(row.get("question", ""))

        if q == question or q in question:
            return str(row.get("answer", "")), 1

    # keyword match
    keywords = q.split()
    for _, row in df.iterrows():
        question = normalize(row.get("question", ""))

        matches = sum(1 for k in keywords if k in question)
        if matches >= max(1, len(keywords)//2):
            return str(row.get("answer", "")), 1

    return None, 0