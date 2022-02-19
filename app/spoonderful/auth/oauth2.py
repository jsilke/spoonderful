from jose import JWTError, jwt  # JSON Web Token handling
from datetime import datetime, timedelta
from app.spoonderful.data import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.spoonderful.config import settings

# from src.spoonderful.app.config import settings
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
SIGNING_ALGORITHM = settings.signing_algorithm
ACCESS_TOKEN_DURATION = settings.access_token_duration_minutes


def create_access_token(data: dict):
    """
    Create a limited duration JSON Web Token using a specified algorithm. Both the algorithm and duration
    (in minutes) can be specified in config.py. The SECRET_KEY is used in conjunction with the other data
    to sign the token to ensure data integrity.
    """
    to_encode = data.copy()

    token_expiry = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    to_encode.update({"exp": token_expiry})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=SIGNING_ALGORITHM)

    return encoded_jwt


def _verify_access_token(token: str, credentials_exception: HTTPException):
    """
    Function used internally by `get_current_user` to verify the user's access token. Raises an exception
    if the user does not exist or if the token cannot be verified.
    """
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[SIGNING_ALGORITHM])
        user_id = data.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=user_id)  # TODO add TokenData to schemas.
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)
):
    """
    Check the current user's id using access token verification.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = _verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
