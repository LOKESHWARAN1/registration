from sqlalchemy.orm import Session

from src import models, schemas


def get_user_by_email(db: Session, email: str):
    return db.query(models.UserPSQL).filter(models.UserPSQL.email == email).first()


def get_user_by_phone(db: Session, phone: str):
    return db.query(models.UserPSQL).filter(models.UserPSQL.phone == phone).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.UserPSQL(
        full_name=user.full_name,
        email=user.email,
        password=user.password,  # Normally you would hash the password
        phone=user.phone
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_profile(db: Session, user_id: int, profile_picture: str):
    db_profile = models.Profile(user_id=user_id, profile_picture=profile_picture)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


def get_user(db: Session, user_id: int):
    return db.query(models.UserPSQL).filter(models.UserPSQL.id == user_id).first()