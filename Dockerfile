# Use a slim Python image for smaller size
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first to leverage caching
COPY requirements.txt .

# Install dependencies without cache to keep image light
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your bot code into the container
COPY . .

# Default command to run your bot
CMD ["python", "main.py"]
