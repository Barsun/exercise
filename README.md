# Exercise AXA

![CI](https://github.com/Barsun/exercise-axa/actions/workflows/ci.yml/badge.svg)

A production-ready Flask application with RESTful API, PostgreSQL database, and observability (Prometheus + Grafana).

## Features
- RESTful API for CRUD operations.
- PostgreSQL database with SQLAlchemy ORM.
- Structured logging with `structlog`.
- Prometheus metrics and Grafana dashboards.
- Dockerized for easy deployment.

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/myapp.git
   cd myapp
   ```
2. Set up environment variables in .env
    ```
    DATABASE_URL=postgresql://user:password@db:5432/mydatabase
    SECRET_KEY=your_secret_key
    ```
3. Start the services:
   ```bash
   docker compose up --build
   ```
4. Access the services:
    - Flask app: http://localhost:5000

5. Observability
    - Prometheus: http://localhost:9090
    - Grafana: http://localhost:3000

## API Documentation
 - Swagger UI: http://localhost:5000/api/docs
