from app.services.docs import extract_text
from app.bot.vector_db import json_to_data, insert_data_to_db
from app.bot.embedding import get_embedding
import json


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    words = text.split()
    chunks = [
        " ".join(words[i : i + chunk_size])
        for i in range(0, len(words), chunk_size - overlap)
    ]
    return chunks


async def process_document(file_path: str, file_type: str, metadata: dict):
    text = extract_text(file_path, file_type)
    chunks = chunk_text(text)
    embeddings = [get_embedding(chunk) for chunk in chunks]
    metadata["chunks"] = [
        {"text": chunk, "embedding": embedding}
        for chunk, embedding in zip(chunks, embeddings)
    ]

    # Save as JSON
    output_path = f"{file_path}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        # print(metadata)
        json.dump(metadata, f, ensure_ascii=False, indent=2, default=str)

    # return output_path
    data = json_to_data(output_path)
    insert_data_to_db(data)


# if __name__ == "__main__":
#     import sys
#     file_path = sys.argv[1]
#     file_type = sys.argv[2]
#     metadata = json.loads(sys.argv[3])
