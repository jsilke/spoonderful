from fastapi import FastAPI, Depends, status
import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    """
    Establish a database session for SQL queries and close the session after. Acts as our dependency.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/recommendations", status_code=status.HTTP_200_OK)
def get_recipes(ingredients: str):
    """
    Query Spoonacular's API for data using the provided ingredient list and apply the recommendation algorithm to return recipe recommendations.
    """
    pass


@app.post("/register", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)) -> None:
    """
    Register a new user with a valid email address and any password.
    """
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
