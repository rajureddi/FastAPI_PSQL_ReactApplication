# FastAPI Copilot Instructions

## Project Overview
This is a FastAPI-based application. FastAPI is a modern Python web framework for building REST APIs with automatic API documentation, type validation, and async support.

## Architecture & Organization

### Structure
- `main.py`: Application entry point and route definitions
- `.github/copilot-instructions.md`: AI agent guidance (this file)

As the project grows, follow this structure:
- `app/main.py`: FastAPI app initialization
- `app/routers/`: API endpoint modules (one file per logical resource)
- `app/models/`: Pydantic schemas for request/response validation
- `app/services/`: Business logic and external service integrations
- `app/database/`: Database configuration and ORM models
- `app/middleware/`: Custom middleware for cross-cutting concerns
- `tests/`: Unit and integration tests

## Key Patterns & Conventions

### Pydantic Models
Define request/response schemas using Pydantic v2:
```python
from pydantic import BaseModel, Field

class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1)
    description: str | None = None
```

### API Route Organization
Group related endpoints in separate router modules:
```python
# app/routers/items.py
from fastapi import APIRouter
router = APIRouter(prefix="/items", tags=["items"])

@router.get("/")
async def list_items():
    pass
```

Then include in main.py:
```python
from fastapi import FastAPI
from app.routers import items

app = FastAPI()
app.include_router(items.router)
```

### Async/Await
Use `async def` for all endpoint handlers to leverage FastAPI's async capabilities:
```python
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return await fetch_from_db(item_id)
```

### Response Status Codes
Explicitly set appropriate HTTP status codes:
```python
@app.post("/items", status_code=201)
async def create_item(item: ItemCreate):
    pass
```

## Development Workflow

### Starting the Application
```powershell
# Install dependencies
pip install fastapi uvicorn

# Run development server with auto-reload
uvicorn main:app --reload

# Access API docs at http://localhost:8000/docs
```

### Testing
```powershell
# Install test dependencies
pip install pytest httpx

# Run tests
pytest
```

## Dependencies & External Services
- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation

## Common Tasks

### Adding a New Endpoint
1. Create a router file in `app/routers/`
2. Define Pydantic models for request/response in `app/models/`
3. Include router in `main.py` with `app.include_router()`
4. Document with docstrings for auto-generated API docs

### Database Integration
When connecting to a database, use SQLAlchemy with async support:
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
```

### Error Handling
Use FastAPI's HTTPException for API errors:
```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
```

## Documentation
- Auto-generated API docs available at `/docs` (Swagger UI)
- Use docstrings in endpoint functions to enhance OpenAPI documentation
- Format: """Description of endpoint"""
