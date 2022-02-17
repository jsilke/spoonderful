from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import app.routes as route


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET, POST"],
    allow_headers=["*"],
)

app.include_router(route.register.router)
app.include_router(route.user.router)
app.include_router(route.login.router)
app.include_router(route.vote.router)
app.include_router(route.recommendation.router)


@app.get("/")
def root():
    return {"message": "Hello World!"}
