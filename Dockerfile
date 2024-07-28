FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y \
    libpq-dev \
    build-essential

COPY requirements.txt /app/
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD ["python", "app.py"]
