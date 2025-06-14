from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..dependencies import get_db

router = APIRouter(prefix="/restaurants", tags=["restaurants"])


@router.get("/", response_model=List[schemas.Restaurant])
def read_restaurants(db: Session = Depends(get_db)):
    return crud.get_restaurants_with_reviews(db)


@router.post("/", response_model=schemas.Restaurant)
def create_restaurant(restaurant: schemas.RestaurantCreate, db: Session = Depends(get_db)):
    return crud.create_restaurant(db, restaurant)


@router.get("/{restaurant_id}", response_model=schemas.RestaurantDetail)
def read_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    db_restaurant = crud.get_restaurant(db, restaurant_id)
    if not db_restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    reviews = crud.get_reviews_by_restaurant(db, restaurant_id)
    avg = (
        sum(r.rating for r in reviews) / len(reviews)
        if reviews else None
    )
    restaurant = schemas.RestaurantDetail.from_orm(db_restaurant)
    restaurant.average_rating = avg
    restaurant.reviews = reviews
    return restaurant


@router.put("/{restaurant_id}", response_model=schemas.Restaurant)
def update_restaurant(restaurant_id: int, restaurant: schemas.RestaurantUpdate, db: Session = Depends(get_db)):
    db_restaurant = crud.update_restaurant(db, restaurant_id, restaurant)
    if not db_restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return db_restaurant
