FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Update and install system dependencies
RUN apt-get update \
  && apt-get install -y --no-install-recommends gcc libpq-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /src

# Install Python dependencies
COPY requirements.txt .

RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

COPY . /src
#RUN pip3 install --no-cache-dir daphne
#RUN pip3 install --no-cache-dir channels channels_redis

# Download the Vosk model (small model for example)
RUN apt-get update && apt-get install -y wget && \
    mkdir model && \
    wget -q -O model/vosk-model-small-en-us-0.15.zip http://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip && \
    unzip model/vosk-model-small-en-us-0.15.zip -d model && \
    mv model/vosk-model-small-en-us-0.15 model/en-us && \
    rm model/vosk-model-small-en-us-0.15.zip

EXPOSE 8000

# Start Daphne server
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "ai_backend.asgi:application"]

