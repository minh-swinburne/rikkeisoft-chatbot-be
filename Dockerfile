FROM python:3.12.9-slim

WORKDIR /

# Install system dependencies required for Tesseract OCR
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

ADD ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./app /app

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
