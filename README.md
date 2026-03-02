# VoxPop (Backend)

Public comment board API (no auth, no database).  
Comments are stored in memory (array) and displayed in a public feed with pagination.

## Tech
- FastAPI
- Uvicorn
- In-memory storage (array)

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload