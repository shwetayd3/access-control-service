# Access Control Service
Backend service responsible for authentication and authorization built with FastAPI, implementing:

- 🔐 JWT-based Authentication
- 🧩 Role-Based Access Control (RBAC)
- 🌐 OAuth2 (Google Login)
- ⚡ Async SQLAlchemy (PostgreSQL)
- 🔄 Database migrations with Alembic
- 🧪 Async Test Suite (pytest + httpx)

## Features

### Authentication
- User registration & login
- Secure password hashing (bcrypt)
- JWT token generation

### Authorization (RBAC)
- Dynamic role assignment
- Role-based route protection
- Dependency-based enforcement (require_role)

### OAuth
Google OAuth2 login integration

### Database
- PostgreSQL with async SQLAlchemy
- Alembic migrations

### Testing
- Async test suite using pytest
- In-memory DB for isolation
- Covers auth + RBAC flows

## 🏗 Architecture Overview
This service is designed to issue JWT tokens, support OAuth-based login and act as a centralized identity provider for internal services.



                ┌──────────────────────┐
                │      Client (UI)     │
                │  Web / Mobile / API  │
                └─────────┬────────────┘
                          │ HTTP Requests
                          ▼
                ┌──────────────────────┐
                │     FastAPI App      │
                │  (app/main.py)       │
                └─────────┬────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │   Auth API   │  │  Roles API   │  │  OAuth API   │
    │ /auth/*      │  │ /roles/*     │  │ /oauth/*     │
    └──────┬───────┘  └──────┬───────┘  └──────┬───────┘
           │                 │                 │
           ▼                 ▼                 ▼
    ┌──────────────────────────────────────────────────┐
    │              Business Logic Layer                │
    │  - JWT handling                                 │
    │  - RBAC enforcement (require_role)              │
    │  - Password hashing (bcrypt)                    │
    └────────────────────────┬─────────────────────────┘
                             │
                             ▼
    ┌──────────────────────────────────────────────────┐
    │          Database Layer (SQLAlchemy Async)       │
    │  - Users                                        │
    │  - Roles                                        │
    │  - UserRoles                                    │
    └────────────────────────┬─────────────────────────┘
                             ▼
                   ┌──────────────────┐
                   │   PostgreSQL DB  │
                   └──────────────────┘
## Tech Stack
- FastAPI
- PostgreSQL (planned)
- JWT + OAuth (planned)


## Project Structure
```
app/
├── api/            # API route handlers
├── auth/           # Authentication logic (JWT, RBAC)
├── core/           # Config, DB, logging, security
├── models/         # SQLAlchemy models
├── schemas/        # Pydantic schemas
├── main.py         # App entrypoint

alembic/            # DB migrations
tests/              # Async test suite
```

### Local Run
```bash
pip install -r requirements.txt
bash scripts/start_dev.sh
