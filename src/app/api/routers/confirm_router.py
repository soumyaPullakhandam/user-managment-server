from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from ...api import schemas, crud
from ..database import SessionLocal
from ..app_utils import confirm_token, generate_token, http_exceptions

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
def confirm_email(data: schemas.EmailToken, db: Session = Depends(get_db)):
    """
      ``/verify`` - Validates the email verification token and
      updates the correspondent user with password and other information:

      Args:
          db (Session) = Depends(get_db): Manages persistence operations for ORM-mapped objects.

          data (schemas.EmailToken): Email verification token to validate the user

      Returns:
          schemas.Token : Returns the authentication token or exceptions.

      """
    email = confirm_token(data.email_token)
    if email is None:
        raise http_exceptions(400, "The confirmation link is invalid or has expired.")
    else:
        user = crud.get_user_by_email(db, email=email)
        if user.is_active:
            raise http_exceptions(400, "Account already confirmed. Please login.")
        else:
            user = crud.set_password(db, user, data)
            return generate_token(user.email)
