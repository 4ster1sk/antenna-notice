FROM mcr.microsoft.com/devcontainers/base:bookworm

RUN apt update \
    && apt upgrade -y \
    && apt -y install python3 python3-pip \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt --break-system-packages