from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True


class ProfileBase(BaseModel):
    profile_picture: str


class ProfileOut(ProfileBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
