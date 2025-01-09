from sentence_transformers import SentenceTransformer

# Load a pre-trained Sentence Transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Input sentences
sentences = ["This is a test sentence.", "Embeddings are easy to generate with Hugging Face."]

# Generate embeddings
embeddings = model.encode(sentences)

print(embeddings.shape)  # Output shape: (number of sentences, embedding size)
