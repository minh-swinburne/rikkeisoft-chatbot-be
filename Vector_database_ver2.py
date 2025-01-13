from pymilvus import connections, DataType, MilvusClient
import ast
import csv

# Connect to Milvus
connections.connect("my_database", host="localhost", port="19530")

client = MilvusClient (
    uri="http://localhost:19530",
    token="root:Milvus"
)

# Define collection name
collection_name = "Document_embeddings"

# Define the schema
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

# Create the collection if it doesn't exist
if collection_name not in client.list_collections():
    client.create_collection(
        collection_name=collection_name,
        schema=schema,
        index_params=index_params
    )


# Load data from the CSV
def load_csv_data(csv_path):
    # data = {"my_id": [], "my_vector": [], "my_varchar": []}
    data = []
    with open(csv_path, mode="r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # Convert my_id to int and my_vector back to a list
            try:
                data.append({
                    "my_id": int(row["my_id"]),
                    "my_vector": ast.literal_eval(row["my_vector"]),
                    "my_varchar": row["my_varchar"]
                })
            except Exception as e:
                print(f"Skipping invalid row: {row}. Error: {e}")
    return data


# Insert data into Milvus
def insert_data_into_milvus(client, data):
    print(len(data[0]["my_vector"]))
    client.insert(
        collection_name=collection_name,
        data=data
        )
    print(f"Inserted {len(data)} records into the collection.")


# Main script
if __name__ == "__main__":
    # Load data from CSV
    csv_path = "output_data.csv"
    try:
        data = load_csv_data(csv_path)

        # Insert data into the Milvus collection
        insert_data_into_milvus(client, data)

        # Optional: Flush to ensure data is persisted
        client.flush(collection_name=collection_name)

        print(f"Data successfully uploaded to the Milvus collection '{collection_name}'.")
    except ValueError as e:
        print(f"Error: {e}")
