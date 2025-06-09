# ─── Dockerfile ────────────────────────────────────────────────────────────────
FROM python:3.10-slim

# 1. Set the working directory
WORKDIR /app

# 2. Copy only requirements first (leverage Docker cache)
COPY requirements.txt .

# 3. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy your bot code (including main.py) into /app
COPY main.py .
# If you have any other .py files or folders, copy them too:
# COPY utils.py .  
# COPY src/ ./src/

# 5. Debug: list /app so you can see exactly which files made it in
RUN echo "---- /app contents ----" && ls -la /app && echo "-----------------------"

# 6. Finally run
CMD ["python", "main.py"]
