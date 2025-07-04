FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1  # Show logs immediately

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
