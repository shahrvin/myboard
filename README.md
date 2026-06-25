# MyBoard — Backend API

A REST API backend for Myboard a personal dashboard to access across all devices. Admins can log in and manage a collection of configurable widgets (notes, links, embeds, etc.) arranged on a board.

## Features

- Single-admin authentication with JWT tokens
- Full CRUD for widgets with position, visibility, and z-index support
- SQLite database with field-level encryption (Fernet AES-128) for sensitive data
- Automatic table creation on startup — no migration step needed for a fresh install

## Tech Stack

| Layer | Library |
|---|---|
| Framework | FastAPI |
| ORM | SQLAlchemy 2 |
| Database | SQLite |
| Auth | JWT via `python-jose`, passwords hashed with `bcrypt` |
| Encryption | `cryptography` (Fernet) |

## Project Structure

```
backend/
├── app/
│   ├── main.py          # FastAPI app, CORS, lifespan
│   ├── config.py        # Settings loaded from .env
│   ├── database.py      # SQLAlchemy engine and session
│   ├── models.py        # ORM models (Admin, Widget)
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── auth.py          # Token creation and verification
│   ├── encryption.py    # EncryptedString / EncryptedJSON column types
│   └── routers/
│       ├── auth.py      # POST /auth/setup, POST /auth/login
│       └── widgets.py   # CRUD under /widgets
├── .env                 # Secret config (never commit this)
├── .gitignore
└── requirements.txt
```

## Setup

### 1. Create and activate a virtual environment

```bash
python3 -m venv env1
source env1/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy the example below into a `.env` file in the `backend/` directory and replace the placeholder values:

```env
DATABASE_URL=sqlite:///./myboard.db
SECRET_KEY=replace-with-a-long-random-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-secure-password
DB_ENCRYPTION_KEY=your-fernet-key-here
```

To generate a secure `SECRET_KEY`:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

To generate a `DB_ENCRYPTION_KEY`:
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 4. Run the server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

## First-time Admin Setup

The `/auth/setup` endpoint can only be called once (it rejects subsequent calls if an admin already exists):

```bash
curl -X POST http://localhost:8000/auth/setup \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your-secure-password"}'
```

## Authentication

All `/widgets` endpoints require a Bearer token. Obtain one by logging in:

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your-secure-password"}'
```

Use the returned token in subsequent requests:

```bash
curl http://localhost:8000/widgets/ \
  -H "Authorization: Bearer <token>"
```

## API Reference

Interactive docs are available at `http://localhost:8000/docs` when the server is running.

| Method | Path | Description |
|---|---|---|
| `POST` | `/auth/setup` | Create the admin account (one-time) |
| `POST` | `/auth/login` | Log in and receive a JWT |
| `GET` | `/widgets/` | List all widgets for the logged-in admin |
| `GET` | `/widgets/{id}` | Get a single widget |
| `POST` | `/widgets/` | Create a widget |
| `PUT` | `/widgets/{id}` | Update a widget |
| `DELETE` | `/widgets/{id}` | Delete a widget |

## Database Encryption

The `username`, `title`, and `data` columns are encrypted at rest using Fernet symmetric encryption. The encryption key is stored in `.env` under `DB_ENCRYPTION_KEY`. Keep this key safe — losing it means the stored data cannot be decrypted.

> **Note:** If you have an existing `myboard.db` with plaintext data, delete it before starting the server with encryption enabled so the tables are recreated clean.
