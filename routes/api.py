
from fastapi import APIRouter, Query
from datetime import datetime
from sqlalchemy import or_
from database import SessionLocal

db = SessionLocal()


router = APIRouter(
    prefix="/api",
    responses={404: {"description": "Not found"}},
    tags=["Api"]
)


@router.get("/", status_code=200)
async def root():
    return {"message": "Welcome to API"}




