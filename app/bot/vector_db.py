from pymilvus import MilvusClient, DataType, connections, db
from app.core.config import settings
from app.bot.model import model
import json

collection_name = settings.milvus_collection

# Connect to Milvus
connections.connect(host=settings.milvus_host, port=settings.milvus_port)

if settings.milvus_db not in db.list_database():
    database = db.create_database(settings.milvus_db)

client = MilvusClient(uri="http://localhost:19530", token="root:Milvus", db_name=settings.milvus_db)


def setup_db():
    if collection_name not in client.list_collections():
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

        client.create_collection(
            collection_name=collection_name,
            schema=schema,
            index_params=index_params
        )

    print(f"Connected to Milvus version {client.get_server_version()}.")
    print(f"Available collections: {client.list_collections()}")


def json_to_data(json_path: str):
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


def insert_data_to_db(data):
    # Insert data
    client.insert(collection_name=collection_name, data=data)
    client.flush(collection_name=collection_name)

    print(f"Inserted {len(data)} records into '{collection_name}'.")


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
        context.append(
            {
                "title": result["entity"].get("title"),
                "text": result["entity"].get("text"),
                "score": result["distance"],
            }
        )

    return context


if __name__ == "__main__":
    json_path = "uploads/COS40005_Unit_Outline_DN_Jan2025.docx.pdf.json"
    data = json_to_data(json_path)
    insert_data_to_db(data)
