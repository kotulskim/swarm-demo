FROM python:3.11-slim

WORKDIR /app
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

EXPOSE 5005

HEALTHCHECK --interval=10s --timeout=3s --retries=3 \
  CMD curl -f http://localhost:5005/health || exit 1

CMD ["python","app.py"]
