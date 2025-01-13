from pymilvus import MilvusClient, DataType, connections
from sentence_transformers import SentenceTransformer
from app.services.docs import extract_text
from app.core.config import settings
import json

model = SentenceTransformer(settings.embedding_model)
dimension = settings.embedding_dimension    # 384

collection_name = "document_embeddings"
# Connect to Milvus
connections.connect("default", host="localhost", port="19530")

client = MilvusClient(uri="http://localhost:19530", token="root:Milvus")


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    words = text.split()
    chunks = [
        " ".join(words[i : i + chunk_size])
        for i in range(0, len(words), chunk_size - overlap)
    ]
    return chunks


def create_embeddings(chunks: list[str]) -> list[list[float]]:
    return [model.encode(chunk).tolist() for chunk in chunks]


def json_to_milvus(json_path: str):
    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    rows = []
    document_id = data["document_id"]
    title = data["title"]
    description = data["description"]
    meta = {
        "categories": data["categories"],
        "creator": data["creator"],
        "created_date": data["created_date"],
        "restricted": data["restricted"],
        "uploader": data["uploader"],
        "uploaded_time": data["uploaded_time"],
    }

    for chunk in data["chunks"]:
        rows.append(
            {
                "document_id": document_id,
                "title": title,
                "description": description,
                "text": chunk["text"],
                "embedding": chunk["embedding"],
                "meta": meta,
            }
        )
    return rows


def insert_data_to_milvus(data):
    # Define the schema
    schema = MilvusClient.create_schema(
        auto_id=False,
        enable_dynamic_field=True,
    )

    # Add fields to the schema
    schema.add_field(
        field_name="embedding_id",
        datatype=DataType.INT64,
        is_primary=True,
        auto_id=True,
    )
    schema.add_field(
        field_name="document_id", datatype=DataType.VARCHAR, max_length=128
    )
    schema.add_field(field_name="title", datatype=DataType.VARCHAR, max_length=512)
    schema.add_field(
        field_name="description", datatype=DataType.VARCHAR, max_length=1024
    )
    schema.add_field(field_name="text", datatype=DataType.VARCHAR, max_length=8192)
    schema.add_field(
        field_name="embedding",
        datatype=DataType.FLOAT_VECTOR,
        dim=settings.embedding_dimension,
    )
    schema.add_field(field_name="meta", datatype=DataType.JSON)  # Metadata

    index_params = client.prepare_index_params()

    index_params.add_index(field_name="embedding", index_type="AUTOINDEX")

    if collection_name not in client.list_collections():
        client.create_collection(
            collection_name=collection_name, schema=schema, index_params=index_params
        )

    # Insert data
    client.insert(collection_name=collection_name, data=data)
    client.flush(collection_name=collection_name)
    print(f"Inserted {len(data)} records into '{collection_name}'.")


async def process_document(file_path: str, file_type: str, metadata: dict):
    text = extract_text(file_path, file_type)
    chunks = chunk_text(text)
    embeddings = create_embeddings(chunks)
    metadata["chunks"] = [
        {"text": chunk, "embedding": embedding}
        for chunk, embedding in zip(chunks, embeddings)
    ]

    # Save as JSON
    output_path = f"{file_path}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        # print(metadata)
        json.dump(metadata, f, ensure_ascii=False, indent=2, default=str)

    # return output_path
    data = json_to_milvus(output_path)
    insert_data_to_milvus(data)


def search_context(user_query: str, top_k: int = 5):
    context = []
    query_embedding = model.encode(user_query).tolist()
    search_results = client.search(
        collection_name=collection_name,
        data=[query_embedding],
        anns_field="embedding",
        limit=top_k,
        search_params={"metric_type": "IP"},
        output_fields=["title", "text"],  # Fetch relevant fields for context
    )

    for result in search_results[0]:
        context.append({
            "title": result["entity"].get("title"),
            "text": result["entity"].get("text"),
            "score": result["distance"],
        })

    return context


# if __name__ == "__main__":
#     import sys
#     file_path = sys.argv[1]
#     file_type = sys.argv[2]
#     metadata = json.loads(sys.argv[3])
