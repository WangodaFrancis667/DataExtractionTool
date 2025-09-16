FROM python:3.11-slim

# system deps for PDF processing tools
RUN apt-get update && apt-get install -y \
    build-essential \
    libxml2-dev \
    libxslt-dev \
    libjpeg-dev \
    zlib1g-dev \
    poppler-utils \
    ghostscript \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# create folders
RUN mkdir -p /app/uploads /app/outputs

COPY . .

ENV FLASK_APP=app
ENV FLASK_ENV=production

# use gunicorn for production
CMD ["gunicorn", "app:create_app()", "-b", "0.0.0.0:8000", "--workers", "3"]
