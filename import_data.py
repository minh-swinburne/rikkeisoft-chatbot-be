import json
import numpy as np
from pymilvus import connections, Collection

# Connect to Zilliz Cloud
CLUSTER_ENDPOINT = "https://in03-b02ef543aa9deb0.serverless.gcp-us-west1.cloud.zilliz.com"
TOKEN = "02c806f88100abdf6faf67e6451944e05769c763ced684bc3a5942320663cd88b8b45426e7f9c2210834d092debacf690eb4446b"

connections.connect(uri=CLUSTER_ENDPOINT, token=TOKEN)

collection = Collection("document_embeddings")

# Open JSONL file for efficient writing
jsonl_file = "exported_vectors.json"

with open(jsonl_file, "r", encoding="utf-8") as fp:
    data = json.load(fp)
    result = collection.insert(data)
    print(f"Imported {len(result)} records...")

print(f"Data export completed! Saved to {jsonl_file}")
