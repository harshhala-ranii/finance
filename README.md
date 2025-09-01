# Finance Dashboard

A Streamlit-based finance tracker with PostgreSQL backend, containerized using Docker.

## Features

- Add monthly balances and expenses
- View balance overview and expense analysis
- Data is persisted in PostgreSQL
- Responsive charts and tables (desktop/tablet recommended)

## Requirements

- Docker & Docker Compose

## Quick Start

1. **Clone the repository**

2. **Build and run with Docker Compose**
   ```
   docker-compose up --build
   ```

3. **Access the app**
   - Open [http://localhost:8501](http://localhost:8501) in your browser

## Project Structure

- `app.py` — Main Streamlit app
- `pages/` — Streamlit page modules
- `db_utils.py` — Database ORM and utility functions
- `requirements.txt` — Python dependencies
- `Dockerfile` — Container build for the app
- `docker-compose.yml` — Multi-container setup (app + PostgreSQL)

## Environment Variables

- The app uses `DB_URL` for database connection, set automatically by Docker Compose.

## Database

- PostgreSQL is used for persistent storage.
- Data is stored in `balances` and `expenses` tables.

## Customization

- Update categories in `app.py` as needed.
- Change database credentials in `docker-compose.yml` if required.

## Troubleshooting

- If you see connection errors, ensure Docker is running and ports 5432/8501 are free.
- For database migrations, update `db_utils.py` and re-build containers.

## License