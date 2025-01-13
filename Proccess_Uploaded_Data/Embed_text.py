import os
import csv
from pymilvus import model
from Extract_file import extract_text_from_file  # Import the extraction functions from the first file

# Initialize SentenceTransformerEmbeddingFunction
sentence_transformer_ef = model.dense.SentenceTransformerEmbeddingFunction(
    model_name='all-MiniLM-L6-v2',
    device='cpu'
)

# Define output CSV path
output_csv_path = "output_data.csv"

def generate_file_id(existing_ids):
    """Generate a unique integer ID based on existing IDs."""
    if existing_ids:
        return max(existing_ids) + 1
    return 1

def chunk_document(text, max_chunk_size=500):
    """
    Split a document into chunks based on paragraphs and word count.
    Each paragraph is processed, and long paragraphs are further split by length.
    """
    paragraphs = text.split("\n\n")  # Split text into paragraphs based on double newlines
    chunks = []
    for paragraph in paragraphs:
        words = paragraph.split()
        for i in range(0, len(words), max_chunk_size):
            chunk = " ".join(words[i:i + max_chunk_size])
            chunks.append(chunk)
    return chunks

def process_files(file_paths):
    """Process files to extract text, chunk it by document structure, and create embeddings."""
    output_data = []

    # Load existing data from CSV if the file exists
    existing_ids = set()
    if os.path.exists(output_csv_path):
        try:
            with open(output_csv_path, mode='r', encoding='utf-8', newline='') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    if "document_id" in row:
                        existing_ids.add(int(row["document_id"]))
                        output_data.append(row)
        except Exception as e:
            print(f"Warning: Could not load existing CSV file: {e}. Starting fresh.")

    for file_path in file_paths:
        try:
            # Extract text from the file
            text = extract_text_from_file(file_path)

            # Chunk the document based on structure
            chunks = chunk_document(text)

            # Process each chunk
            for chunk in chunks:
                chunk_id = generate_file_id(existing_ids)

                # Create embeddings for the chunk
                embedding = sentence_transformer_ef.encode_documents([chunk])[0]

                # Append the chunk metadata and embedding to output
                output_data.append({
                    "document_id": chunk_id,
                    "document_name": os.path.basename(file_path),  # Keep track of the document name
                    "my_vector": embedding.tolist(),  # Store only embeddings
                })
                existing_ids.add(chunk_id)  # Add the new ID to the set

        except ValueError as e:
            print(f"Error processing {file_path}: {e}")

    # Save the updated data to the CSV file
    with open(output_csv_path, mode='w', encoding='utf-8', newline='') as csv_file:
        fieldnames = ["document_id", "document_name", "my_vector"]
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write the header only if the file is empty
        csv_writer.writeheader()

        # Write the rows
        for data in output_data:
            # Make sure 'my_vector' is in string format since CSV cannot handle list directly
            data["my_vector"] = str(data["my_vector"])
            csv_writer.writerow(data)

    print(f"Data saved to {output_csv_path}")

# Example usage
if __name__ == "__main__":
    file_paths = ["example_2.pdf"]  # List of file paths to process
    process_files(file_paths)
