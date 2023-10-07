from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import event,auth,approve
from fastapi.staticfiles import StaticFiles
from database import SessionLocal,engine
import os
import models


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


app=FastAPI()


origins = [
    "http://localhost",
    "http://localhost:3000"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)


attachments_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "attachments")
app.mount("/attachments", StaticFiles(directory=attachments_folder_path), name="attachments")


app.include_router(auth.router)

app.include_router(event.router)

app.include_router(approve.router)

