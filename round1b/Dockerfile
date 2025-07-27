FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
 && apt-get clean

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["python", "/app/main.py"]
