from sqlalchemy import Column, Integer, String
from app.config.database import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "msteroid"}


    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)