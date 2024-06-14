from jose import jwt, JWTError
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import redis
from .config import settings
from . import models, schemas, database


SECRET_KEY= settings.secret_key
ALGORITHM= settings.algorithm
AECCESS_TOKEN_EXPIRE_MINUTES= settings.access_token_expire_minutes

oauth2_scheme= OAuth2PasswordBearer(tokenUrl="login")

redis_client = redis.Redis(host=settings.redis_host, port=settings.redis_host, db=0)

def create_access_token(data, scope:str):
    to_encode= data.copy()
    expire= datetime.now()+ timedelta(minutes=AECCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encode_jwt= jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

def verify_access_token(token:str, credentials_exception):
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = str(payload.get("user_id"))
        token_data= schemas.TokenData(id=user_id)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str= Depends(oauth2_scheme), db:Session = Depends(database.get_db)):
    credentials_exception= HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could Not Valid Credentials", headers={"WWW-Authenticate": "Bearer"})
    token= verify_access_token(token, credentials_exception)
    user= db.query(models.Users).filter(models.Users.id == token.id).first()
    return user
        
