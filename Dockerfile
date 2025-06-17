FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m myuser
RUN chown -R myuser:myuser /app
USER myuser

EXPOSE 8000

CMD ["gunicorn", "shop_api.wsgi:application", "--bind", "0.0.0.0:8000"] 