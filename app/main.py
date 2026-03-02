from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from app.routers.comments import router as comments_router
from app.routers.ui import router as ui_router

app = FastAPI(title="VoxPop", version="1.0.0")

app.state.templates = Jinja2Templates(directory="app/templates")

app.include_router(comments_router)
app.include_router(ui_router)

@app.get("/")
def root():
    return {"message": "VoxPop API is running. Go to /docs or /ui"}