import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from sqlalchemy.orm import Session

from . import schemas
from .app_utils import generate_confirmation_token
from .models import UserInfo


def get_user_by_email(db: Session, email: str):
    """
      To get the user by email:

      Args:
          db (Session): Manages persistence operations for ORM-mapped objects.

          email (str): to filter email.

      Returns:
          SetPassword: returns the filtered user using email.

      """
    return db.query(UserInfo).filter(UserInfo.email == email).first()


def set_password(db: Session, user: schemas.SetPassword, data: schemas.EmailToken):
    """
      It generates the secured password, add the password to the correspondent user.
       Encrypts the pass using ``CryptContext`` :

      Args:
          db (Session): Manages persistence operations for ORM-mapped objects.

          user (schemas.SetPassword): To add the data to the correspondent user

          data (schemas.EmailToken) : data contains email verification token and user entered password

      Returns:
          SetPassword: returns the filtered user using email.

      """

    hashed_password = schemas.pwd_context.hash(data.password)
    user.password = hashed_password
    user.is_active = True
    import datetime
    user.activate_on = datetime.datetime.now()
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_user(db: Session, user: schemas.UserCreate):
    """
      It creates the new user and send the verification email to user registered email-id.
      ``SendGridAPIClient`` passes with verification email id with verification token url:

      Args:
          db (Session): Manages persistence operations for ORM-mapped objects.

          user (schemas.UserCreate): User given data

      Returns:
          UserCreate: created user.

    """

    db_user = UserInfo(fullname=user.fullname, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    token = generate_confirmation_token(user.email)

    message = Mail()
    message.from_email = 'soumya4v@gmail.com'
    message.dynamic_template_data = {"token": token, "fullname": user.fullname,
                                     "UIPath": str(os.environ.get("UI_HOST_URL_SENDGRID"))}
    message.to = user.email
    message.subject = 'Please confirm your email id'
    message.template_id = str(os.environ.get("SENDGRID_TEMPLATE_ID"))

    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

    return db_user


def check_username_password(db: Session, user: schemas.UserAuthenticate):
    """
      To match the user entered password with encrypted password:

      Args:
          db (Session): Manages persistence operations for ORM-mapped objects.

          user (schemas.UserAuthenticate): User given credentials

      Returns:
          bool: If password matches returns True.

      """

    db_user_info: UserInfo = get_user_by_email(db, email=user.email)
    return schemas.pwd_context.verify(user.password, db_user_info.password)
