from pymilvus import MilvusClient, DataType

# Connect to Milvus server
client = MilvusClient(
    uri="http://localhost:19530",
    token="root:Milvus"
)

# Sample collection schemas
schemas = {
    "user_profiles": {
        "auto_id": False,
        "enable_dynamic_field": False,
        "fields": [
            {"field_name": "user_id", "datatype": DataType.INT64, "is_primary": True},
            {"field_name": "embedding", "datatype": DataType.FLOAT_VECTOR, "dim": 128},
            {"field_name": "age", "datatype": DataType.INT64},
        ],
    },
    "products": {
        "auto_id": True,
        "enable_dynamic_field": False,
        "fields": [
            {"field_name": "product_id", "datatype": DataType.INT64, "is_primary": True},
            {"field_name": "vector", "datatype": DataType.FLOAT_VECTOR, "dim": 64},
            {"field_name": "description", "datatype": DataType.VARCHAR, "max_length": 1024},
        ],
    },
    "text_documents": {
        "auto_id": True,
        "enable_dynamic_field": True,
        "fields": [
            {"field_name": "doc_id", "datatype": DataType.INT64, "is_primary": True},
            {"field_name": "text_vector", "datatype": DataType.FLOAT_VECTOR, "dim": 256},
            {"field_name": "title", "datatype": DataType.VARCHAR, "max_length": 256},
        ],
    },
}

# Function to create collections
for collection_name, schema_config in schemas.items():
    # Create a schema object
    schema = client.create_schema(
        auto_id=schema_config["auto_id"],
        enable_dynamic_field=schema_config["enable_dynamic_field"],
    )
    for field in schema_config["fields"]:
        schema.add_field(**field)

    # Create the collection with the correct method signature
    client.create_collection(collection_name, schema=schema)
    print(f"Collection '{collection_name}' created.")

# List and verify created collections
collections = client.list_collections()
print("Available Collections:", collections)
