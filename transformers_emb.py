from sentence_transformers import SentenceTransformer

# Load the embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# Function to generate embeddings
def generate_embeddings(text):
    return embedding_model.encode(text)
