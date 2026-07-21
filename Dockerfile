FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    vim \
    wget \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ARG USERNAME=hp
ARG USER_GROUP=app-user
RUN groupadd $USER_GROUP && \
    useradd -m -g $USER_GROUP -s /bin/bash $USERNAME && \
    usermod -aG sudo $USERNAME && \
    echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

RUN playwright install chromium && playwright install-deps

COPY . .

RUN python -m ITviec.py 
