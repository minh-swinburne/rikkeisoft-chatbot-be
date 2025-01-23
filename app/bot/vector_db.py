from pymilvus import MilvusClient, DataType, connections, db
from app.bot.embedding import get_embedding
from app.core.config import settings

collection_name = settings.milvus_collection

# Connect to Milvus
# connections.connect(host=settings.milvus_host, port=settings.milvus_port)

# if settings.milvus_db not in db.list_database():
#     database = db.create_database(settings.milvus_db)

client = MilvusClient(uri=settings.milvus_uri, token=settings.milvus_token)


def setup_vector_db():
    if not client.has_collection(collection_name):
        # Define the schema
        schema = client.create_schema(
            auto_id=True,
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
            collection_name=collection_name, schema=schema, index_params=index_params
        )

    print(f"Connected to Milvus version {client.get_server_version()}.")
    print(f"Available databases: {client.list_databases()}")
    print(f"Available collections: {client.list_collections()}")


def insert_data(data):
    # Insert data
    result = client.insert(collection_name=collection_name, data=data)
    client.flush(collection_name=collection_name)

    print(f"Inserted {result["insert_count"]} records into '{collection_name}'.")
    return result["insert_count"]


def delete_data(doc_id: str):
    result = client.delete(
        collection_name=collection_name,
        filter=f"document_id == '{doc_id}'",
    )

    print(f"Deleted {result["delete_count"]} embeddings of document with ID '{doc_id}'.")
    return result["delete_count"]


def search_context(user_query: str, top_k: int = 5):
    context = []
    query_embedding = get_embedding(user_query)
    search_results = client.search(
        collection_name=collection_name,
        data=[query_embedding],
        anns_field="embedding",
        limit=top_k,
        search_params={"metric_type": "COSINE"},
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


def query_document(title: str):
    query_results = client.query(
        collection_name=collection_name,
        filter=f'title == "{title}"',
        output_fields=["description", "meta"],
        limit=1,
    )

    return query_results[0] if query_results else None
