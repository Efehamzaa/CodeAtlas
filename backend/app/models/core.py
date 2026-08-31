from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    github_id = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    repositories = relationship("Repository", back_populates="owner_user")

class Repository(Base):
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True, index=True)
    user_id= Column(Integer, ForeignKey("users.id"))
    github_url=Column(String)
    name = Column(String)
    owner = Column(String)
    default_branch = Column(String , default="main")
    status = Column(String , default="Pending")

    owner_user = relationship("User", back_populates="repositories")

    analyses = relationship("Analysis", back_populates="repository")