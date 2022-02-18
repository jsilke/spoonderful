from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from src.spoonderful.app.data import database, models, schemas

router = APIRouter(prefix="/user", tags=["Users"])


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(
    id: int,
    db: Session = Depends(database.get_db),
):
    """
    Checks the user table for a user with the specified id and returns the user information.
    """
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} does not exist",
        )

    return user
