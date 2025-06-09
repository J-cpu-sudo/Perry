# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy dependencies and code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run your bot
CMD ["python", "main.py"]
