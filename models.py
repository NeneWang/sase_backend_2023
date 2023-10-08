
from email.policy import default
from sqlalchemy import PrimaryKeyConstraint, String,Boolean,Integer,Column, Table,Text, DateTime, ARRAY, Identity, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import datetime, uuid
import shortuuid
from sqlalchemy.ext.declarative import declarative_base
from database import Base
from sqlalchemy import func



import json
Base = declarative_base()

from pydantic import BaseModel
from typing import List, Optional



# Define the User model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    guid = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    tags = Column(ARRAY(String))
    languages = Column(ARRAY(String))
    last_active = Column(DateTime, default=func.now(), nullable=False)



# Define the Thread model
class Thread(Base):
    __tablename__ = 'threads'

    thread_id = Column(Integer, primary_key=True, autoincrement=True)
    guid = Column(String, nullable=False)
    body = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_time = Column(DateTime, nullable=False)
    tags = Column(ARRAY(String))

    # Define a relationship with the User model
    user = relationship("users", back_populates="threads")


    


