from typing import List

import pymongo
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import src.crud as crud
import src.models as models
import src.schemas as schemas
from src import crud_psql
from src.database import SessionLocal, engine
from decouple import config

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# MongoDB setup
mongo_client = pymongo.MongoClient(config('MONGO_URI'))
mongo_db = mongo_client[config('MONGO_DB')]
profile_collection = mongo_db[config('MONGO_COLLECTION')]


@app.post("/register/", response_model=schemas.User,
          tags=['PSQL And MongoDB'],
          description="Register user details in psql db and upload the profile image into mongo db")
async def create_user(
        email: str = Form(...),
        full_name: str = Form(...),
        phone: str = Form(...),
        password: str = Form(...),
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    db_user = crud.get_user_by_email(db, email=email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_create = schemas.UserCreate(
        email=email,
        full_name=full_name,
        phone=phone,
        password=password
    )
    user_id = crud.create_user(db=db, user=user_create)

    # Save profile picture in MongoDB
    profile_picture_id = profile_collection.insert_one({
        "user_id": user_id,
        "profile_picture": await file.read()
    }).inserted_id

    return crud.get_user(db, user_id=user_id)


@app.get("/users/", response_model=List[schemas.User],
         tags=['PSQL And MongoDB'],
         description="Get registered user details and unique user_id for both database")
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.post("/user-register/", response_model=schemas.UserOut,
          tags=['PSQL'],
          description="Register user details in the psql db")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud_psql.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = crud_psql.get_user_by_phone(db, phone=user.phone)
    if db_user:
        raise HTTPException(status_code=400, detail="Phone number already registered")

    new_user = crud_psql.create_user(db=db, user=user)
    return new_user


@app.post("/upload-profile-picture/{user_id}/", response_model=schemas.ProfileOut,
          tags=['PSQL'],
          description="Upload the profile picture in the psql db")
async def upload_profile_picture(user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_location = f"profile_pictures/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    profile = crud_psql.create_profile(db=db, user_id=user_id, profile_picture=file_location)
    return profile


@app.get("/get-users/{user_id}/", response_model=schemas.UserOut,
         tags=['PSQL'],
         description="Get registered user details in the psql db")
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_psql.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
