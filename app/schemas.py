from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ReviewBase(BaseModel):
    rating: float = Field(..., ge=0.0, le=5.0)
    comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    restaurant_id: int
    user_id: str


class ReviewUpdate(ReviewBase):
    pass


class Review(ReviewBase):
    id: int
    user_id: str
    created_at: datetime

    class Config:
        orm_mode = True


class RestaurantBase(BaseModel):
    name: str
    address: str
    lat: float
    lng: float


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantUpdate(RestaurantBase):
    pass


class Restaurant(RestaurantBase):
    id: int
    created_at: datetime
    reviews: List[Review] = []

    class Config:
        orm_mode = True


class RestaurantDetail(Restaurant):
    average_rating: Optional[float] = None
