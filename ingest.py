# ingest.py
import pandas as pd
from mongoconnection import insert_many, ensure_indexes, collection
from datetime import datetime
import os

CSV_PATH = os.getenv("CSV_PATH", r"C:\Users\gupta\Desktop\BDA_Project\tweets_data.csv")

def ingest_csv(csv_path=CSV_PATH, limit=None):
    df = pd.read_csv(csv_path, encoding="ISO-8859-1", header=None)
    # If your CSV has header adjust accordingly
    # Example: assume columns [target, id, date, flag, user, text]
    # If your CSV structure is different adjust explicit columns.
    if df.shape[1] >= 6:
        df = df[[0,5]]
        df.columns = ["target", "text"]
    else:
        df.columns = ["text"]
    records = []
    for i, row in df.iterrows():
        rec = {
            "text": str(row.get("text", "")),
            "target": row.get("target", None),
            "created_at": datetime.utcnow(),  # replace if CSV has timestamp
            "user": None
        }
        records.append(rec)
        if limit and len(records) >= limit:
            break
    insert_many(records)
    ensure_indexes()
    print(f"Inserted {len(records)} documents")

if __name__ == "__main__":
    ingest_csv()
