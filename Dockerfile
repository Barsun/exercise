# Build stage
FROM python:3.9-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage
FROM python:3.9-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH
ENV FLASK_APP=app:app
ENV FLASK_ENV=production

EXPOSE 5000
EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:5050", "--workers", "4", "--threads", "2", "app:app"]