# APIPractice

A REST API built with FastAPI, PostgreSQL, and SQLAlchemy. Covers user authentication (JWT), CRUD for posts, and password hashing with bcrypt.

## Prerequisites

- Python 3.10+
- PostgreSQL (running locally on port 5432)

## Setup

### 1. Clone and enter the repo

```bash
git clone <repo-url>
cd APIPractice
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install fastapi sqlalchemy psycopg[binary] pydantic python-jose[cryptography] passlib[bcrypt]
```

> Save these for teammates: `pip freeze > requirements.txt`

### 4. Set up the PostgreSQL database

Open psql or pgAdmin and run:

```sql
CREATE DATABASE fastapi;
```

### 5. Update database credentials

In [app/database.py](app/database.py), replace the connection string with your own credentials:

```python
SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@localhost/fastapi'
```

Also update the hardcoded credentials in [app/main.py](app/main.py) to match.

### 6. Run the server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

## API Docs

FastAPI generates interactive docs automatically:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
app/
├── main.py            # App entry point, router registration
├── database.py        # SQLAlchemy engine and session setup
├── models.py          # Database table definitions (Post, User)
├── schemas.py         # Pydantic request/response schemas
├── oauth2.py          # JWT token creation and verification
├── utils.py           # Password hashing helpers
└── routers/
    ├── post.py        # Post CRUD endpoints
    ├── user.py        # User creation endpoints
    └── authentication.py  # Login endpoint
```
