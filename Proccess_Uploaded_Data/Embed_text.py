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

def process_files(file_paths):
    """Process files to extract text and create embeddings."""
    output_data = []

    # Load existing data from CSV if the file exists
    existing_ids = set()
    if os.path.exists(output_csv_path):
        try:
            with open(output_csv_path, mode='r', encoding='utf-8', newline='') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    if "my_id" in row:
                        existing_ids.add(int(row["my_id"]))
                        output_data.append(row)
        except Exception as e:
            print(f"Warning: Could not load existing CSV file: {e}. Starting fresh.")

    for file_path in file_paths:
        file_id = generate_file_id(existing_ids)
        if file_id in existing_ids:
            print(f"File with ID {file_id} has already been processed. Skipping.")
            continue

        try:
            # Extract text from the file
            text = extract_text_from_file(file_path)

            # Create embeddings from the extracted text
            embedding = sentence_transformer_ef.encode_documents([text])[0]  # Encode the text and get the first embedding

            # Append the data to output
            output_data.append({
                "my_id": file_id,
                "my_vector": embedding.tolist(),  # Convert NumPy array to list for serialization
                "my_varchar": text[:100]  # Example: store the first 100 characters of the text
            })
            existing_ids.add(file_id)  # Add the new ID to the set
        except ValueError as e:
            print(f"Error processing {file_path}: {e}")

    # Save the updated data to the CSV file
    with open(output_csv_path, mode='w', encoding='utf-8', newline='') as csv_file:
        fieldnames = ["my_id", "my_vector", "my_varchar"]
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
