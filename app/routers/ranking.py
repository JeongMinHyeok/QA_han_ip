from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..dependencies import get_db

router = APIRouter(prefix="/ranking", tags=["ranking"])


@router.get("/", response_model=List[schemas.RestaurantDetail])
def get_ranking(limit: int = Query(10, gt=0), db: Session = Depends(get_db)):
    ranking = crud.get_ranking(db, limit)
    results = []
    for restaurant, avg_rating in ranking:
        item = schemas.RestaurantDetail.from_orm(restaurant)
        item.average_rating = avg_rating
        results.append(item)
    return results
