# from app.core.config import settings
# import json

# collection_name = "document_embeddings"


# def json_to_milvus(json_path: str):
#     with open(json_path, "r", encoding="utf-8") as file:
#         data = json.load(file)

#     rows = []
#     document_id = data["document_id"]
#     title = data["title"]
#     description = data["description"]
#     meta = {
#         "categories": data["categories"],
#         "creator": data["creator"],
#         "created_date": data["created_date"],
#         "restricted": data["restricted"],
#         "uploader": data["uploader"],
#         "uploaded_time": data["uploaded_time"],
#     }

#     for chunk in data["chunks"]:
#         rows.append(
#             {
#                 "document_id": document_id,
#                 "title": title,
#                 "description": description,
#                 "text": chunk["text"],
#                 "embedding": chunk["embedding"],
#                 "meta": meta,
#             }
#         )
#     return rows


# def insert_data_to_milvus(data):
#     # Connect to Milvus
#     connections.connect("default", host="localhost", port="19530")

#     client = MilvusClient(uri="http://localhost:19530", token="root:Milvus")
#     # Define the schema
#     schema = MilvusClient.create_schema(
#         auto_id=False,
#         enable_dynamic_field=True,
#     )

#     # Add fields to the schema
#     schema.add_field(field_name="embedding_id", datatype=DataType.INT64, is_primary=True, auto_id=True)
#     schema.add_field(field_name="document_id", datatype=DataType.VARCHAR, max_length=128)
#     schema.add_field(field_name="title", datatype=DataType.VARCHAR, max_length=512)
#     schema.add_field(field_name="description", datatype=DataType.VARCHAR, max_length=1024)
#     schema.add_field(field_name="text", datatype=DataType.VARCHAR, max_length=8192)
#     schema.add_field(field_name="embedding", datatype=DataType.FLOAT_VECTOR, dim=settings.embedding_dimension)
#     schema.add_field(field_name="meta", datatype=DataType.JSON)  # Metadata

#     index_params = client.prepare_index_params()

#     index_params.add_index(field_name="embedding", index_type="AUTOINDEX")

#     if collection_name not in client.list_collections():
#         client.create_collection(
#             collection_name=collection_name,
#             schema=schema,
#             index_params=index_params
#             )

#     # Insert data
#     client.insert(collection_name=collection_name, data=data)
#     client.flush(collection_name=collection_name)
#     print(f"Inserted {len(data)} records into '{collection_name}'.")


# def search_context(user_query: str, top_k: int = 5):
#     query_embedding = model.encode(user_query).tolist()
#     result


# if __name__ == "__main__":
#     json_path = "uploads/COS40005_Unit_Outline_DN_Jan2025.docx.pdf.json"
#     data = json_to_milvus(json_path)
#     insert_data_to_milvus(data)
