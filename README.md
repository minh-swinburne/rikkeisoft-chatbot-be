# Rikkeisoft - Documents Chatbot Assistant for Employees | Backend

Language: Python
Framework: FastAPI

## Installation & Launch

1. Ensure you have Python and `venv` package installed.
2. Clone this repository to your local machine.
3. Create a virtual environment:

   ```
   python -m venv venv
   ```
4. Activate the virtual environment:

   * On Windows:

     ```
     .\venv\Scripts\activate
     ```
   * On macOS and Linux:

     ```
     source venv/bin/activate
     ```

5. Install required packages:
  ```
    pip install -r requirements.txt
  ```

6. Create a `.env` file in the root dir (where this file is in) and provide these environment variables:
  ```
    GROQ_API_KEY
    UPLOAD_DIR (optional)
  ```

7. Compose Docker containers with this command:
  ```
    docker compose up -d
  ```

  This will prepare the Milvus vector database.

8. Launch the FastAPI server:
  ```
    fastapi dev app.py
  ```

9. Server should be running at <http://127.0.0.1:8000>. APIs can be tested at <http://127.0.0.1:8000/docs>

## Development Guidance

To save tree structure of a directory, run command:
  ```
    tree /f /a [<drive>:][<path>] > [<drive>:]/[<file_path>]/<filename>.txt
  ```