from fastapi import FastAPI
from app.routes import router
from app.services.db_init import initialize_database
from contextlib import asynccontextmanager
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan function to handle startup and shutdown events.
    """
    if os.getenv("INIT_DB", "true").lower() == "true":
        await initialize_database()

    yield  # Yield control back to FastAPI


app = FastAPI(lifespan=lifespan)

# Include the routes from the `routes.py` file
app.include_router(router)
