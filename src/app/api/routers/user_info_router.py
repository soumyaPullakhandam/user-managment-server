from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from ...api import schemas, crud
from ..database import SessionLocal
from ..app_utils import decode_access_token, http_exceptions

router = APIRouter()


# Dependency
def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get("/", response_model=schemas.UserCreate)
def read_own_items(user: schemas.UserCreate = Depends(decode_access_token), db: Session = Depends(get_db)):
    """
      ``/user-info`` - To get the user information:

      Args:
          db (Session) = Depends(get_db): Manages persistence operations for ORM-mapped objects.

          user (schemas.UserCreate) = Depends(decode_access_token):
            Dependency injection is to verify the authentication access token.

      Returns:
          schemas.UserCreate : Returns the user information or exception.

      """
    if user is None:
        raise http_exceptions(400, "The token is invalid or has expired.")
    else:
        email = user.get('sub')
        user = crud.get_user_by_email(db, email=email)
        if user is None:
            raise http_exceptions(400, "Please login to generate a new token.")
        else:
            return {"fullname": user.fullname, "email": user.email}
