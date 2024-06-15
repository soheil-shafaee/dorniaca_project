from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum
import re

class GenderEnum(str, Enum):
    FEMALE= "FEMALE"
    MALE= "MALE"
    NOT_SPECIFIED= "NOT_SPECIFIED"

class UserCreate(BaseModel):
    userName: str
    fullName: Optional[str]= None
    email: EmailStr
    hashedPassword: str
    DoB: Optional[str]= None
    gender: Optional[GenderEnum]= GenderEnum.NOT_SPECIFIED
    createdAt: Optional[datetime]= None
    updatedAt: Optional[datetime]=None

    @field_validator('DoB')
    def parse_dob(cls, value):
        if value:
            try:
                return datetime.strptime(value, "%m-%d-%Y").date()
            except ValueError:
                raise ValueError("Birth(DoB) Must be in month-day-year format")
        return value
    @field_validator("hashedPassword")
    def validate_password(cls, v):
        if v is not None:
            if len(v) <8:
                raise ValueError("Password must be at least 8 charachter long")
            if not re.search(r"[0-9]", v):
                    raise ValueError('Password must contain at least one digit')
            if not re.search(r"[A-Z]", v):
                    raise ValueError('Password must contain at least one uppercase letter')
            if not re.search(r"[a-z]", v):
                    raise ValueError('Password must contain at least one lowercase letter')
            if not re.search(r"[@#$%^&+=]", v):
                    raise ValueError('Password must contain at least one special character (@, #, $, %, ^, &, +, =)')
        return v 
    
    class Config:
        orm_mode= True

class UserUpdate(UserCreate):
    hashedPassword: Optional[str]= None
    @field_validator("hashedPassword")
    def validate_password(cls, v):
        if v is not None:
            if len(v) <8:
                raise ValueError("Password must be at least 8 charachter long")
            if not re.search(r"[0-9]", v):
                    raise ValueError('Password must contain at least one digit')
            if not re.search(r"[A-Z]", v):
                    raise ValueError('Password must contain at least one uppercase letter')
            if not re.search(r"[a-z]", v):
                    raise ValueError('Password must contain at least one lowercase letter')
            if not re.search(r"[@#$%^&+=]", v):
                    raise ValueError('Password must contain at least one special character (@, #, $, %, ^, &, +, =)')
        return v 
    


class UserOutPublic(BaseModel):
    id:int
    userName:str
    createdAt:datetime

    class Config:
        orm_mode= True

class UserOutPrivate(BaseModel):
    id:int
    userName:str
    fullName:Optional[str]= None
    email:EmailStr
    DoB:Optional[datetime]= None
    gender:GenderEnum
    createdAt:datetime
    updatedAt:Optional[datetime]= None

    class Config:
        orm_mode= True


# ---------- Listing Section -------------
class TypeEnum(str, Enum):
    HOUSE= "HOUSE"
    APARTMENT= "APARTMENT"

class BaseListing(BaseModel):
    type:TypeEnum
    availableNow: Optional[bool]= True
    address:str
    ownerId:Optional[int]=None
    createdAt:Optional[datetime]=None
    updatedAt:Optional[datetime]= None

    class Config:
        orm_mode= True
    
class CreateListing(BaseListing):
     pass

class UpdateListing(BaseModel):
    type:Optional[TypeEnum] = None
    availableNow: Optional[bool]= True
    address:Optional[str]= None
    ownerId:Optional[int]=None
    createdAt:Optional[datetime]=None
    updatedAt:Optional[datetime]= None

    class Config:
        orm_mode= True

class ListingOut(BaseModel):
    id:int
    type:str
    avaiableNow:Optional[bool] = True
    address:str
    createdAt:datetime
    updatedAt:Optional[datetime]=None

    class Config:
        orm_mode= True

class ListingOutUpdate(BaseModel):
    id:int
    type:TypeEnum
    avaiableNow:Optional[bool] = True
    ownerId:Optional[int]= None
    address:str
    createdAt:Optional[datetime]= None
    updatedAt:Optional[datetime]=None

    class Config:
        orm_mode= True

class Token(BaseModel):
    access_token:str
    type_token:str

class TokenData(BaseModel):
    id: Optional[str]=None
