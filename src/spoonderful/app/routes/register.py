from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session
from src.spoonderful.app.auth import utils
from src.spoonderful.app.data import database, models, schemas

router = APIRouter(prefix="/register", tags=["Sign Up"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """
    Create a new user. Note that since emails are our usernames and we have forced them to be unique,
    duplicates will result in an error.
    """

    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user  # TODO change.
