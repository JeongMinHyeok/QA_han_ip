import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from .database import Base, engine
from .routers import ranking, restaurants, reviews

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="QA 맛집 지도", description="QA팀 검증 맛집 정보 API")

templates = Jinja2Templates(directory="app/templates")

app.include_router(restaurants.router)
app.include_router(reviews.router)
app.include_router(ranking.router)


@app.get("/map", response_class=HTMLResponse)
async def show_map(request: Request):
    api_key = os.getenv("GOOGLE_API_KEY")
    return templates.TemplateResponse(
        "map.html", {"request": request, "google_api_key": api_key}
    )
