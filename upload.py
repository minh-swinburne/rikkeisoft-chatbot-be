from fastapi import FastAPI, UploadFile, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId

app = FastAPI()

# MongoDB Configuration for Atlas
MONGO_URL = "mongodb+srv://lamdoanquang21:helloyouguy123@cluster0.ak53g.mongodb.net/"
DATABASE_NAME = "FileStorage"
COLLECTION_NAME = "File"

client = AsyncIOMotorClient(MONGO_URL)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Allowed file types
ALLOWED_CONTENT_TYPES = [
    "video/mp4", "video/mkv", "application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", 
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/msword", "application/vnd.ms-excel"
]

@app.post("/upload/")
async def upload_file(file: UploadFile):
    try:
        # Check file type
        if file.content_type not in ALLOWED_CONTENT_TYPES:
            raise HTTPException(status_code=400, detail=f"File type '{file.content_type}' is not allowed.")

        # Read file content
        file_content = await file.read()

        # Create a file record to insert into MongoDB
        file_record = {
            "filename": file.filename,
            "content_type": file.content_type,
            "data": file_content
        }

        # Insert the record and return the inserted ID
        result = await collection.insert_one(file_record)
        return {"message": "File uploaded successfully", "file_id": str(result.inserted_id)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files/{file_id}")
async def get_file(file_id: str):
    try:
        # Find the file by its ID in the collection
        file_record = await collection.find_one({"_id": ObjectId(file_id)})
        
        if not file_record:
            raise HTTPException(status_code=404, detail="File not found")

        # Return file metadata and content
        return {
            "filename": file_record["filename"],
            "content_type": file_record["content_type"],
            "data": file_record["data"].decode("utf-8")  # Convert binary data to string if necessary
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

