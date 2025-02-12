from pymilvus import MilvusClient, DataType, WeightedRanker, AnnSearchRequest, connections, db
from app.bot.embedding import get_embedding
from app.core.settings import settings

collection_name = settings.milvus_collection

# Connect to Milvus
# connections.connect(host=settings.milvus_host, port=settings.milvus_port)

# if settings.milvus_db not in db.list_database():
#     database = db.create_database(settings.milvus_db)

for _ in range(5):
    try:
        client = MilvusClient(uri=settings.milvus_host, token=settings.milvus_token)
        print(f"✅ Connected to Milvus version {client.get_server_version()}.")
        print(f"Available databases: {client.list_databases()}")
        print(f"Available collections: {client.list_collections()}")
        break
    except Exception as e:
        print(f"❌ Failed to connect to Milvus: {e}")


def setup_vector_db():
    try:
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
            schema.add_field(field_name="text", datatype=DataType.VARCHAR, max_length=8192)
            schema.add_field(
                field_name="embedding",
                datatype=DataType.FLOAT_VECTOR,
                dim=settings.embedding_dimension,
            )

            index_params = client.prepare_index_params()

            index_params.add_index(field_name="embedding", index_type="AUTOINDEX")

            client.create_collection(
                collection_name=collection_name, schema=schema, index_params=index_params
            )
        print(f"✅ Milvus collection setup successfully.")
    except Exception as e:
        print(f"❌ Failed to setup Milvus: {e}")


def insert_data(data):
    # Insert data
    try:
        result = client.insert(collection_name=collection_name, data=data)
        client.flush(collection_name=collection_name)

        print(f"📤 Inserted {result["insert_count"]} records into collection '{collection_name}' of Milvus.")
        return result["insert_count"]
    except Exception as e:
        print(f"❌ Failed to insert data into Milvus: {e}")
        return 0


def delete_data(doc_id: str):
    try:
        result = client.delete(
            collection_name=collection_name,
            filter=f"document_id == '{doc_id}'",
        )

        print(f"🗑️ Deleted {result["delete_count"]} embeddings of document with ID '{doc_id}' from collection '{collection_name}' of Milvus.")
        return result["delete_count"]
    except Exception as e:
        print(f"❌ Failed to delete data from Milvus: {e}")
        return 0


def search_context(messages: list[str], top_k: int = 5, weight: float = 0.8) -> list[dict]:
    context = []
    weights = [(1 - weight)] * (len(messages) - 1)
    weights.append(weight)
    qa_embeddings = get_embedding(messages)
    search_results = client.hybrid_search(
        collection_name=collection_name,
        ranker=WeightedRanker(*weights),
        limit=top_k,
        output_fields=["document_id", "text"],
        reqs=[
            AnnSearchRequest(
                data=[embedding],
                anns_field="embedding",
                param={"metric_type": "COSINE", "params": {"nprobe": 10}},
                limit=top_k,
            )
            for embedding in qa_embeddings
        ],
    )
    print(f"🔍 Found {len(search_results[0])} similar documents in Milvus.")
    # print(qa_embeddings)

    for result in search_results[0]:
        context.append(
            {
                "document_id": result["entity"].get("document_id"),
                "text": result["entity"].get("text"),
                "score": result["distance"],
            }
        )

    return context
