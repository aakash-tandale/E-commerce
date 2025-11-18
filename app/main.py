from fastapi import FastAPI
from app.db import init_db
from app.routers import coupons

app = FastAPI()

init_db()

app.include_router(coupons.router)
