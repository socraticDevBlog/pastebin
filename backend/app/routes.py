from typing import Optional
from fastapi import APIRouter, HTTPException, Request

from app.models import PasteModel, PasteDataAware
from app.mock_db import mock_db

router = APIRouter()


@router.get("/api/v1/pastes")
async def get_pastes(client_id: Optional[str] = None, request: Request = None):
    """
    GET /api/pastes
    Retrieve pastes for a specific client.
    """
    if not client_id:
        client_id = request.client.host  # Use client IP as fallback
    client_pastes = [
        paste for paste in mock_db.values() if paste.get("client_id") == client_id
    ]
    return {"pastes": client_pastes}


@router.get("/api/v1/{id}")
async def get_paste(id: str, request: Request):
    """
    GET /api/v1/{id}
    Retrieve a specific paste by ID.
    """
    paste = mock_db.get(id)
    if not paste:
        raise HTTPException(status_code=404, detail="Paste not found")
    user_agent = request.headers.get("User-Agent", "")
    is_web_browser = "Mozilla" in user_agent or "AppleWebKit" in user_agent
    return {"paste": paste, "is_web_browser": is_web_browser}


@router.post("/api/v1")
async def create_paste(paste: PasteModel, request: Request):
    """
    POST /api/v1
    Create a new paste.
    """
    client_id = paste.workspace if paste.workspace != "" else request.client.host
    data = PasteDataAware(content=paste.content, client_id=client_id)
    mock_db[data.id] = {
        "id": data.id,
        "content": data.content,
        "client_id": data.client_id,
        "created_at": data.created_at,
    }
    return {"id": data.id}


@router.options("/api/v1")
async def options_api():
    """
    OPTIONS /api
    Return allowed methods for the /api route.
    """
    return {"methods": ["GET", "POST", "OPTIONS"]}
