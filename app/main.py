from fastapi import FastAPI

from .database import Base, engine
from .routers import ranking, restaurants, reviews

Base.metadata.create_all(bind=engine)

app = FastAPI(title="QA 맛집 지도", description="QA팀 검증 맛집 정보 API")

app.include_router(restaurants.router)
app.include_router(reviews.router)
app.include_router(ranking.router)
