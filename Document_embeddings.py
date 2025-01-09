from sentence_transformers import SentenceTransformer
import numpy as np
import argparse
import os
import json
from PyPDF2 import PdfReader
from docx import Document


def extract_text_from_file(file_path):
    """
    Extract text from a file (.txt, .docx, .pdf).

    Parameters:
        file_path (str): Path to the input file.

    Returns:
        str: Extracted text from the file.
    """
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == ".txt":
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    elif file_extension == ".docx":
        doc = Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])

    elif file_extension == ".pdf":
        reader = PdfReader(file_path)
        return "\n".join([page.extract_text() for page in reader.pages])

    else:
        raise ValueError(f"Unsupported file format: {file_extension}")


def generate_embeddings(sentences, model_name="all-MiniLM-L6-v2"):
    """
    Generate vector embeddings for a list of sentences.

    Parameters:
        sentences (list of str): List of sentences to embed.
        model_name (str): Name of the pre-trained model to use for embeddings.

    Returns:
        np.ndarray: A 2D array where each row is the embedding of a sentence.
    """
    # Load the pre-trained model
    model = SentenceTransformer(model_name)

    # Generate embeddings
    embeddings = model.encode(sentences, convert_to_numpy=True)
    return embeddings


def generate_document_embedding(document, model_name="all-MiniLM-L6-v2", aggregation="mean"):
    """
    Generate a document-level embedding by aggregating sentence embeddings.

    Parameters:
        document (str): The document to embed.
        model_name (str): Name of the pre-trained model to use for embeddings.
        aggregation (str): Aggregation method ('mean', 'max').

    Returns:
        np.ndarray: The aggregated document embedding.
    """
    # Split document into sentences
    sentences = document.split(". ")  # Simple sentence splitting by period

    # Generate embeddings for sentences
    sentence_embeddings = generate_embeddings(sentences, model_name)

    # Aggregate embeddings
    if aggregation == "mean":
        document_embedding = np.mean(sentence_embeddings, axis=0)
    elif aggregation == "max":
        document_embedding = np.max(sentence_embeddings, axis=0)
    else:
        raise ValueError("Unsupported aggregation method: Choose 'mean' or 'max'")

    return document_embedding


def save_embeddings(embeddings, output_file, file_format="npy"):
    """
    Save the embeddings to a file.

    Parameters:
        embeddings (np.ndarray): The embeddings to save.
        output_file (str): Path to the output file.
        file_format (str): Format to save the embeddings ('npy', 'txt', 'json').
    """
    if file_format == "npy":
        np.save(output_file, embeddings)
        print(f"Embeddings saved to {output_file}")
    elif file_format == "txt":
        np.savetxt(output_file, embeddings, delimiter=",")
        print(f"Embeddings saved to {output_file}")
    elif file_format == "json":
        with open(output_file, "w", encoding="utf-8") as json_file:
            json.dump(embeddings.tolist(), json_file)
        print(f"Embeddings saved to {output_file}")
    else:
        raise ValueError("Unsupported file format: Choose 'npy', 'txt', or 'json'")


def main():
    parser = argparse.ArgumentParser(description="Generate vector embeddings for sentences or documents.")
    parser.add_argument("--mode", type=str, choices=["sentence", "document"], required=True, help="Choose embedding mode: sentence or document.")
    parser.add_argument("--input", type=str, required=True, help="Path to the input file containing text.")
    parser.add_argument("--output", type=str, required=True, help="Path to save the embeddings.")
    parser.add_argument(
        "--model", type=str, default="all-MiniLM-L6-v2", help="Name of the SentenceTransformer model to use."
    )
    parser.add_argument(
        "--aggregation", type=str, default="mean", choices=["mean", "max"], help="Aggregation method for document embeddings."
    )
    parser.add_argument(
        "--format", type=str, default="npy", choices=["txt", "json"], help="File format to save embeddings."
    )

    args = parser.parse_args()

    # Extract text from input file
    input_text = extract_text_from_file(args.input)

    if args.mode == "sentence":
        # Generate sentence embeddings
        sentences = [input_text]
        embeddings = generate_embeddings(sentences, args.model)
    elif args.mode == "document":
        # Generate document embedding
        embeddings = generate_document_embedding(input_text, args.model, args.aggregation)

    # Save embeddings
    save_embeddings(embeddings, args.output, args.format)


if __name__ == "__main__":
    main()
