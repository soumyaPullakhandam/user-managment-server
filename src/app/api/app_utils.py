import os
import jwt

from datetime import timedelta, datetime

from fastapi import Depends, HTTPException
from itsdangerous import URLSafeTimedSerializer
from ..api.schemas import oauth2_scheme

ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    """
      To generate the token authentication using ``jwt.encode`` method and ``algorithm "HS256"``:

      Args:
          data (dict): User data to create a access token.

          expires_delta (timedelta): To handle access token expiry time.

      Returns:
          str: encoded token.

      """
    secret_key = os.environ.get("SECRET_KEY_APP")
    algorithm = "HS256"
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def decode_access_token(token: str = Depends(oauth2_scheme)):
    """
      To decode the token authentication:

      Args:
          token (str): the token to decode.

      Returns:
          dict: If the token is valid, returns decoded_jwt, else None.
          decoded_jwt contains email-id and expiry time

      """
    secret_key = os.environ.get("SECRET_KEY_APP")
    algorithm = "HS256"
    try:
        decoded_jwt = jwt.decode(jwt=token, key=secret_key, algorithms=[algorithm])
    except:
        return None
    return decoded_jwt


def generate_token(email):
    """
          To generate the token authentication:

          Args:
              email (str): user email-id to generate the token authentication.

          Returns:
              dict: decoded information, contains email-id and expiry time.

    """

    from datetime import timedelta
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "Bearer"}


def generate_confirmation_token(email: str):
    """
          To generate the email verification token using ``itsdangerous``:

          Args:
              email (str): user email-id to generate the email verification token authentication.

          Returns:
              str: return the generated email verification token.

    """
    serializer = URLSafeTimedSerializer(str(os.environ.get('SECRET_KEY')))
    return serializer.dumps(email, salt=str(os.environ.get('SECRET_KEY_SALT')))


def confirm_token(token: str, expiration=3600):
    """
          To verify the email verification token using ``itsdangerous``:

          Args:
              token (str): verify the email verification token.

              expiration (int) : Expiry time of email verification token.

          Returns:
              str: If token valid, then returns email-id else None

    """
    serializer = URLSafeTimedSerializer(str(os.environ.get('SECRET_KEY')))
    try:
        email = serializer.loads(
            token,
            salt=str(os.environ.get('SECRET_KEY')),
            max_age=expiration
        )
    except:
        return None
    return email


def http_exceptions(status_code: int, detail: str):
    """
          To handle http exceptions:

          Args:
              status_code (int): Exception error code.

              detail (str): Exception message

          Returns:
              HTTPException: returns HTTPException

    """
    return HTTPException(status_code=status_code, detail=detail, headers={"WWW-Authenticate": "Bearer"})
