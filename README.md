# Access Control Service
Backend service responsible for authentication and authorization. 

This service is designed to issue JWT tokens, support OAuth-based login, 
and act as a centralized identity provider for internal services.

### Tech Stack
- FastAPI
- PostgreSQL (planned)
- JWT + OAuth (planned)

### Local Run
```bash
pip install -r requirements.txt
bash scripts/start_dev.sh