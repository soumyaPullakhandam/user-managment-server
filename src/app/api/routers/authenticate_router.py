from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from ...api import schemas, crud
from ..database import SessionLocal
from ..app_utils import generate_token, http_exceptions

router = APIRouter()


# Dependency
def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Token)
def authenticate_user(user: schemas.UserAuthenticate, db: Session = Depends(get_db)):
    """
      ``/sign-in`` - Authenticates the user credentials and returns the token or exceptions:

      Args:
          db (Session) = Depends(get_db): Manages persistence operations for ORM-mapped objects.

          user (schemas.UserAuthenticate): User given credentials

      Returns:
          schemas.Token : Returns the token or exceptions.

      """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user is None:
        raise http_exceptions(400, "Entered email was not found.")
    elif db_user.is_active is False:
        raise http_exceptions(400, "Please verify your email using activation link.")
    else:
        is_password_correct = crud.check_username_password(db, user)
        if is_password_correct is False:
            raise http_exceptions(404, "Password is not correct.")
        else:
            return generate_token(user.email)
