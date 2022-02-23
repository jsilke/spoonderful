from fastapi import FastAPI
from .data import models
from .data.database import engine
from .routes import (
    register,
    user,
    login,
    vote,
    recommendation,
)
from fastapi.middleware.cors import CORSMiddleware

# Create tables in the database from the ORM models if they do not exist.
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = [
    "http://localhost.savefood.xyz",
    "https://localhost.savefood.xyz",
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(register.router)
app.include_router(user.router)
app.include_router(login.router)
app.include_router(vote.router)
app.include_router(recommendation.router)


@app.get("/")
def root():
    return {
        "message": "Visit https://savefood.xyz/docs to view documentation and try out the API!"
    }
