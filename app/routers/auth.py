from fastapi import APIRouter, Depends, status, HTTPException, Request
from fastapi_limiter.depends import RateLimiter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..oauth2 import oauth2

from ..schemas import schemas

from ..models import models
from ..utils import utils
from ..database.database import get_db

whitelist_account = []

router= APIRouter(tags=["Authentication"])

async def account_whitelist_rate(request: Request, form_data:OAuth2PasswordRequestForm= Depends()):
    if form_data.username in whitelist_account:
        return
    await RateLimiter(time=5, seconds=60)(request)


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm= Depends(), db: Session = Depends(get_db)):
    user= db.query(models.Users).filter(models.Users.userName == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    if not utils.verify:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    access_token= oauth2.create_access_token(data={"user_id": user.id}, scope=[])
    print(user.userName)
    return {"access_token": access_token, "type_token": "bearer"}
    
