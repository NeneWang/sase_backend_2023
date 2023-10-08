
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

@router.get("/getMeme", status_code=200)
def getMeme():
    return {
        "title": "Made a meal out of it",
        "url": "https://i.redd.it/84uhwvgmmrsb1.gif",
        "preview": [
            "https://preview.redd.it/84uhwvgmmrsb1.gif?width=640&crop=smart&format=png8&s=c12d2e21057a6e7f9868762943c093ea17eba207"
        ]
        }




