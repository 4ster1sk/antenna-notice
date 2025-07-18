FROM python:3.13.5-slim-bookworm

RUN apt update && \
    apt upgrade -y && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt --break-system-packages

CMD ["python3", "/app/main.py"]