FROM python:3.10-slim

# 1. Set working directory
WORKDIR /app

# 2. Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy your Python script into the container
COPY main.py .

# 4. (Optional) Copy your .env file if used by the app
COPY .env .env

# 5. List the directory for debugging (shows up in Railway logs)
RUN echo "Listing /app contents:" && ls -la /app

# 6. Run the bot
CMD ["python", "main.py"]
