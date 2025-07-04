from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    tier = Column(String)  # "free", "pro", "premium"
    requests_today = Column(Integer, default=0)
    last_request_date = Column(DateTime)
