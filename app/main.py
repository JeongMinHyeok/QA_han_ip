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
    client_id = os.getenv("X-NCP-APIGW-API-KEY-ID")
    return templates.TemplateResponse(
        "map.html", {"request": request, "ncp_client_id": client_id}
    )
