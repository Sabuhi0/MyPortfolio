FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Railway (and most PaaS) inject PORT and route traffic to it; 8080 is the local default.
ENV PORT=8080
EXPOSE 8080

CMD ["sh", "-c", "gunicorn run:app --bind 0.0.0.0:${PORT:-8080}"]
