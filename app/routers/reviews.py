from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..dependencies import get_db

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.post("/", response_model=schemas.Review)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    return crud.create_review(db, review)


@router.put("/{review_id}", response_model=schemas.Review)
def update_review(review_id: int, data: schemas.ReviewUpdate, db: Session = Depends(get_db)):
    db_review = crud.update_review(db, review_id, data)
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review


@router.get("/", response_model=List[schemas.Review])
def read_reviews(restaurant_id: int = Query(...), db: Session = Depends(get_db)):
    return crud.get_reviews_by_restaurant(db, restaurant_id)
