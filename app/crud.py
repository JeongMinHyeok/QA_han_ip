from sqlalchemy import func
from sqlalchemy.orm import Session

from . import models, schemas


def get_restaurants_with_reviews(db: Session):
    return (
        db.query(models.Restaurant)
        .join(models.Review)
        .group_by(models.Restaurant.id)
        .all()
    )


def create_restaurant(db: Session, restaurant: schemas.RestaurantCreate):
    db_restaurant = models.Restaurant(**restaurant.dict())
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant


def get_restaurant(db: Session, restaurant_id: int):
    return db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()


def update_restaurant(db: Session, restaurant_id: int, restaurant: schemas.RestaurantUpdate):
    db_restaurant = get_restaurant(db, restaurant_id)
    if not db_restaurant:
        return None
    for field, value in restaurant.dict().items():
        setattr(db_restaurant, field, value)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant


def create_review(db: Session, review: schemas.ReviewCreate):
    # upsert by user_id and restaurant_id
    db_review = (
        db.query(models.Review)
        .filter(models.Review.restaurant_id == review.restaurant_id, models.Review.user_id == review.user_id)
        .first()
    )
    if db_review:
        db_review.rating = review.rating
        db_review.comment = review.comment
    else:
        db_review = models.Review(**review.dict())
        db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def update_review(db: Session, review_id: int, data: schemas.ReviewUpdate):
    db_review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not db_review:
        return None
    for field, value in data.dict().items():
        setattr(db_review, field, value)
    db.commit()
    db.refresh(db_review)
    return db_review


def get_reviews_by_restaurant(db: Session, restaurant_id: int):
    return (
        db.query(models.Review)
        .filter(models.Review.restaurant_id == restaurant_id)
        .all()
    )


def get_ranking(db: Session, limit: int = 10):
    subquery = (
        db.query(
            models.Review.restaurant_id,
            func.avg(models.Review.rating).label("avg_rating"),
            func.count(models.Review.id).label("count_reviews"),
        )
        .group_by(models.Review.restaurant_id)
        .subquery()
    )

    return (
        db.query(models.Restaurant, subquery.c.avg_rating)
        .join(subquery, models.Restaurant.id == subquery.c.restaurant_id)
        .filter(subquery.c.count_reviews >= 2)
        .order_by(subquery.c.avg_rating.desc())
        .limit(limit)
        .all()
    )
