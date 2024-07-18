import re

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from ...api import schemas, crud
from ..database import SessionLocal
from ..app_utils import http_exceptions

router = APIRouter()


# Dependency
def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.UserInfo)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
      ``/sign-up`` - To register new user:

      Args:
          db (Session) = Depends(get_db): Manages persistence operations for ORM-mapped objects.

          user (schemas.UserCreate): User given email-id and fullname

      Returns:
          schemas.UserInfo : Returns the user data and sends the verification email to given email-id
           or exceptions.

      """
    if not re.match(r"[^@]+@[^@]+\.[^@]+", user.email):
        raise http_exceptions(status_code=400, detail="Please verify your email-id.")
    else:
        db_user = crud.get_user_by_email(db, email=user.email)
        if db_user:
            raise http_exceptions(status_code=400, detail="Email already registered.")
        return crud.create_user(db=db, user=user)
