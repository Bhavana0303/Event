from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import event,auth,approve


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

app.include_router(auth.router)

app.include_router(event.router)

app.include_router(approve.router)

