from sentence_transformers import SentenceTransformer

# Load the embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# Function to generate embeddings
def generate_embeddings(text):
    return embedding_model.encode(text)


if __name__ == "__main__":
    # Example usage
    embeddings = generate_embeddings("Hello, world! How are you?")
    print(embeddings)