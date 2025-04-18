from fastapi import FastAPI
from app.routes import router

app = FastAPI()

# Include the routes from the `routes.py` file
app.include_router(router)
