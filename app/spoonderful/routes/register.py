from fastapi import status, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.spoonderful.auth import utils
from app.spoonderful.data import database, models, schemas


router = APIRouter(tags=["Sign Up"])


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut
)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """
    Register to gain access to voting on valid recipes. Note email validation here requires x@y.z format where traditionally:
    x = account
    y = domain
    z = extension

    but here these conventions are not enforced and no confirmation emails are currently sent. This is really just a placeholder
    for unique usernames that gave me a chance to play with an email string validation strategy.
    """

    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password

    try:
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A user with that email is already registered!",
        )

    return new_user
