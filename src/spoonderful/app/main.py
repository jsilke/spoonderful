from fastapi import FastAPI, Depends, status, HTTPException
from app import schemas, models, utils, oauth2  # TODO utils and oauth2
from app.database import engine, get_db
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# TODO Refactor to routes. Fix imports.


@app.get("/recommendations", status_code=status.HTTP_200_OK)
def get_recipes(ingredients: str):
    """
    Query Spoonacular's API for data using the provided ingredient list and apply the recommendation algorithm to return recipe recommendations.
    """
    pass


@app.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut
)  # TODO add UserOut
def create_user(
    user: schemas.CreateUser, db: Session = Depends(get_db)
) -> schemas.UserOut:
    """
    Register a new user with a valid email address and any password.
    """
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.post("/login", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):

    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials."
        )

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials."
        )

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/user/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user(
    id: int,
    db: Session = Depends(get_db),
) -> schemas.UserOut:
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {id} does not exist.",
        )

    return user
