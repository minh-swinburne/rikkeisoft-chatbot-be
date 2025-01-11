from pymilvus import connections, db, DataType, MilvusClient

conn = connections.connect(host="127.0.0.1", port=19530)

client = MilvusClient (
    uri="http://localhost:19530",
    token="root:Milvus"
)

db.using_database("my_database")
db.list_database()

# 3.1. Create schema
schema = MilvusClient.create_schema(
    auto_id=False,
    enable_dynamic_field=True,
)

schema.add_field(field_name="my_id", datatype=DataType.INT64, is_primary=True)
schema.add_field(field_name="my_vector", datatype=DataType.FLOAT_VECTOR, dim=384)
schema.add_field(field_name="my_varchar", datatype=DataType.VARCHAR, max_length=512)

index_params = client.prepare_index_params()

index_params.add_index(
    field_name="my_id",
    index_type="STL_SORT"
)

index_params.add_index(
    field_name="my_vector",
    index_type="AUTOINDEX",
)

client.create_collection(
    collection_name="test",
    schema=schema,
    index_params=index_params
)

res = client.get_load_state(
    collection_name="test"
)

print(res)


