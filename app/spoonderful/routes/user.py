from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from app.spoonderful.data import database, models, schemas
from app.spoonderful.auth import oauth2

router = APIRouter(prefix="/user", tags=["Users"])


@router.get("/", response_model=schemas.UserOut)
def get_user_info(
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Returns the account information of the signed in user.
    """
    user_info = db.query(models.User).filter(models.User.id == current_user.id).first()

    return user_info


@router.get("/votes")
def get_user_votes(
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Returns the votes of the signed in user.
    """
    user_info = (
        db.query(models.Vote.recipe_id, models.Vote.direction)
        .filter(models.Vote.user_id == current_user.id)
        .all()
    )

    return user_info
