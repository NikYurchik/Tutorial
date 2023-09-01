import re
from ipaddress import ip_address
from typing import Callable

import redis.asyncio as redis
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from fastapi.middleware.cors import CORSMiddleware

from src.database.db import get_db
from src.routes import contacts, auth, users

app = FastAPI()


@app.on_event("startup")
async def startup():
    r = await redis.Redis(host='localhost', port=6379, db=0, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(r)


app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')
app.include_router(users.router, prefix='/api')


origins = [ 
    "http://localhost:8000/",
    "http://127.0.0.1:8000/",
    "http://0.0.0.0:8000/"
    ]

ALLOWED_IPS = [
    ip_address('0.0.0.0'),
    ip_address("127.0.0.1")
    ]

user_agent_ban_list = [r"Python-urllib"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.middleware('http')
# async def custom_middleware(request: Request, call_next):
#     # print(f'request.base_url: {request.base_url}')
#     base_url = request.base_url
#     if base_url not in origins:
#         return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "Not allowed base_url"})
#     response = await call_next(request)
#     return response


@app.middleware("http")
async def limit_access_by_ip(request: Request, call_next: Callable):
    # print(f'request.client.host: {request.client.host}')
    ip = ip_address(request.client.host)
    if ip not in ALLOWED_IPS:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "Not allowed IP address"})
    response = await call_next(request)
    return response


@app.middleware("http")
async def user_agent_ban_middleware(request: Request, call_next: Callable):
    user_agent = request.headers.get("user-agent")
    print(f'user_agent: {user_agent}')
    for ban_pattern in user_agent_ban_list:
        if re.search(ban_pattern, user_agent):
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "You are banned"})
    response = await call_next(request)
    return response


templates = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse, description="Main Page", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def root(request: Request):
    return templates.TemplateResponse('index.html', {"request": request, "title": "Contacts App"})


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
