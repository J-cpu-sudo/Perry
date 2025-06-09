FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/main.py .

RUN echo "---- /app contents ----" && ls -la /app && echo "-----------------------"

CMD ["python", "main.py"]
