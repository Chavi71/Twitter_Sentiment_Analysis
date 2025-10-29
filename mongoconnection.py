# db.py
from pymongo import MongoClient, TEXT, ASCENDING
from datetime import datetime
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "twitter_db")
COL_NAME = os.getenv("COL_NAME", "tweets")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COL_NAME]

def ensure_indexes():
    # Full text index on tweet text, plus index on timestamp and geopoint if present
    collection.create_index([("text", TEXT)], name="text_idx", default_language="english")
    collection.create_index([("created_at", ASCENDING)], name="created_at_idx")
    # If geo field exists as {lat,lon} create 2dsphere index
    if "geo" in collection.find_one() or True:  # safe to attempt; if no geo the index is harmless
        try:
            collection.create_index([("geo", "2dsphere")], name="geo_idx")
        except Exception:
            pass

def insert_many(records):
    # records: list of dicts
    for r in records:
        # Normalize minimum fields
        r.setdefault("ingested_at", datetime.utcnow())
    return collection.insert_many(records)

def find_by_query_text(query, limit=1000, start_date=None, end_date=None, geo_filter=None):
    q = {"$text": {"$search": query}} if query else {}
    if start_date or end_date:
        q["created_at"] = {}
        if start_date:
            q["created_at"]["$gte"] = start_date
        if end_date:
            q["created_at"]["$lte"] = end_date
    if geo_filter:
        q["geo"] = {"$near": {"$geometry": {"type": "Point", "coordinates": geo_filter["coordinates"]},
                              "$maxDistance": geo_filter.get("max_distance", 50000)}}
    cursor = collection.find(q, {"text":1,"created_at":1,"user":1,"geo":1,"predicted_sentiment":1,"analysis_meta":1}).limit(limit)
    return list(cursor)

def aggregate_sentiment_for_query(query, start_date=None, end_date=None):
    match = {"$text": {"$search": query}} if query else {}
    if start_date or end_date:
        match["created_at"] = {}
        if start_date:
            match["created_at"]["$gte"] = start_date
        if end_date:
            match["created_at"]["$lte"] = end_date
    pipeline = [
        {"$match": match},
        {"$group": {"_id": "$predicted_sentiment", "count": {"$sum": 1}}},
    ]
    return list(collection.aggregate(pipeline))

def save_analysis_results(doc_id, predicted_sentiment, meta):
    return collection.update_one(
        {"_id": doc_id},
        {"$set": {
            "predicted_sentiment": predicted_sentiment,
            "analysis_meta": meta
        }}
    )
