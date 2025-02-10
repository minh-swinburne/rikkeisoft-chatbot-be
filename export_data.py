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

with open(jsonl_file, "w", encoding="utf-8") as fp:
    iterator = collection.query_iterator(
        batch_size=100,  # Use larger batch sizes for efficiency
        expr="embedding_id >= 0",
        output_fields=["embedding", "document_id", "text"]
    )

    while True:
        result = iterator.next()
        if not result:
            iterator.close()
            break

        # Convert NumPy float32 to JSON-compatible format
        for record in result:
            record["embedding"] = np.array(record["embedding"]).tolist()  # Convert vector to list

            # Write each record as a separate JSON line
            fp.write(json.dumps(record) + "\n")

        print(f"Exported {len(result)} records...")

print(f"Data export completed! Saved to {jsonl_file}")
