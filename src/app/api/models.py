from sqlalchemy import Column, Integer, String, Boolean, Date
from .database import Base


class UserInfo(Base):
    """
      `` User Model ``

    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    fullname = Column(String(50))
    is_active = Column(Boolean, default=False)
    activate_on = Column(Date)

