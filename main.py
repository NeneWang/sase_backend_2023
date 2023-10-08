import uvicorn
from fastapi import FastAPI, Depends, File, UploadFile, Path, status, BackgroundTasks, HTTPException

# from http.client import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine
import models
import os, json
from routes import utils, api



from sqlalchemy.ext.declarative import declarative_base
from fastapi_crudrouter import SQLAlchemyCRUDRouter

from fastapi.openapi.docs import get_swagger_ui_html


dotusername = os.getenv("USER")

app = FastAPI(
    docs_url=None,
    title="DD API",
    description='Bla description',
    )

@app.get("/docs", include_in_schema=False)
async def swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="DD API",
    )


Base = declarative_base()

def get_db():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    finally:
        session.close()


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(utils.router)
app.include_router(api.router)

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def index():
    return { "message": "hello world This is the Another update version"}

if __name__ == "__main__":
    uvicorn.run(app, port=8080, host='0.0.0.0')


@app.get('/unprotected')
def unprotected():
    return { 'hello': 'world' }

