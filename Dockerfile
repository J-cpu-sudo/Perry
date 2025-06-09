# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your main Python script into the container
COPY main.py .

# Copy your .env file if your app needs it (optional, be careful with secrets)
# COPY .env .

# Command to run your app
CMD ["python", "main.py"]
