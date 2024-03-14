FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Update and install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc libffi-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /src

# Install Python dependencies
COPY requirements.txt .

RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

COPY . /src

EXPOSE 8000

# Start Daphne server
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "ai_backend.asgi:application"]

