from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .data import models
from .data.database import engine
from .routes import (
    register,
    user,
    login,
    vote,
    recommendation,
)

# Create tables in the database from the ORM models if they do not exist.
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET, POST"],
    allow_headers=["*"],
)

app.include_router(register.router)
app.include_router(user.router)
app.include_router(login.router)
app.include_router(vote.router)
app.include_router(recommendation.router)


@app.get("/")
def root():
    return {"message": "Hello World!"}
