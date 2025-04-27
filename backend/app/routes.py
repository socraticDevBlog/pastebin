from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.models import PasteInputModel, PasteModel, PasteDataAware
from app.services.dependencies import get_db_client


router = APIRouter()


@router.get("/api/v1/pastes", response_model=List[str])
async def get_pastes(
    client_id: Optional[str] = None,
    request: Request = None,
    db_client=Depends(get_db_client),
):
    """
    GET /api/pastes
    Retrieve pastes for a specific client.
    """
    if not client_id:
        client_id = request.client.host  # Use client IP as fallback
    pastes = await db_client.get_pastes(client_id)
    return [str(paste.paste_id) for paste in pastes]


@router.get("/api/v1/{id}")
async def get_paste(id: str, request: Request, db_client=Depends(get_db_client)):
    """
    GET /api/v1/{id}
    Retrieve a specific paste by ID.
    """
    paste = await db_client.get_paste(id)
    if paste is None:
        raise HTTPException(status_code=404, detail="Paste not found")
    user_agent = request.headers.get("User-Agent", "")
    is_web_browser = "Mozilla" in user_agent or "AppleWebKit" in user_agent

    paste_model = PasteModel(
        content=paste.plain_content(),
        paste_id=paste.paste_id,
        workspace=paste.client_id,
    )

    return paste_model


@router.post("/api/v1", status_code=status.HTTP_201_CREATED)
async def create_paste(
    paste: PasteInputModel, request: Request, db_client=Depends(get_db_client)
):
    """
    POST /api/v1
    Create a new paste.
    """
    client_id = paste.workspace if paste.workspace != "" else request.client.host
    data = PasteDataAware(content=paste.content, client_id=client_id)
    paste_id = await db_client.insert_paste(data)

    return {"id": paste_id}


@router.options("/api/v1")
async def options_api():
    """
    OPTIONS /api
    Return allowed methods for the /api route.
    """
    return {"methods": ["GET", "POST", "OPTIONS"]}
