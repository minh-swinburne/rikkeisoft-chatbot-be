import json
import numpy as np
from pymilvus import connections, Collection

# Connect to Zilliz Cloud
CLUSTER_ENDPOINT = (
    "https://in03-ba4be7d339568a9.serverless.gcp-us-west1.cloud.zilliz.com"
)
TOKEN = "684e6d7a4e9f0bafc9fb20c87cdc1ff6e26af28b7ec253534d72ec5f2701e986800f706746ee3ab377e014ddb8dfa52a170f2e1d"

connections.connect(uri=CLUSTER_ENDPOINT, token=TOKEN)

collection = Collection("document_embeddings")

# Open JSONL file for efficient writing
jsonl_file = "exported_vectors.json"

with open(jsonl_file, "r", encoding="utf-8") as fp:
    data = json.load(fp)
    result = collection.insert(data)
    print(f"Imported {result["insert_count"]} records...")

print(f"Data export completed! Saved to {jsonl_file}")
