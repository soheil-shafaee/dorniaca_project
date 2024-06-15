from fastapi import FastAPI, Request, HTTPException, status
from datetime import datetime
import uvicorn
import redis
import logging
from .config.config import settings
from .routers import users, listing, auth, weather
from .models import models
from .database.database import engine

models.Base.metadata.create_all(bind=engine)



redis_client= redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

allowed_ip_list = ["127.0.0.1"]

app= FastAPI()

async def check_allowed_ip(request:Request, call_next):
    client_ip = request.client.host
    if client_ip not in allowed_ip_list:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access Forbidden")
    return await call_next(request)

app.middleware("http")(check_allowed_ip)


async def dispath(request: Request, call_next):
    client_ip = request.client.host
    request_path = request.url.path
    log_message= f"Request from {client_ip} to {request_path} at {datetime.now()}\n"
    logging.info(log_message)
    with open("login.txt", "a") as file:
        file.write(log_message)
    response = await call_next(request)
    return response
    
app.middleware('http')(dispath)

app.include_router(router=users.router)
app.include_router(router=listing.router)
app.include_router(router=auth.router)
app.include_router(router=weather.router)

@app.get("/")
async def get_info():
    return {"Hello"}

with open("count.txt", "r+") as file:
    counter = int(file.readline())
    file.seek(0)
    file.write(str(counter + 1))

if __name__== "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=3000)