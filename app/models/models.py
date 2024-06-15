from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Date, Enum, event
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from ..database.database import Base
import enum


class Gender(enum.Enum):
    FEMALE="FEMALE"
    MALE="MALE"
    NOT_SPECIFIED="NOT_SPECIFIED"

class Type(enum.Enum):
    HOUSE= "HOUSE"
    APARTMENT= "APARTMENT"

class Users(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, nullable=False)
    userName=Column(String, nullable=False)
    fullName=Column(String, nullable=True)
    email=Column(String, nullable=False)
    hashedPassword=Column(String, nullable=False)
    DoB=Column(Date, nullable=True)
    gender=Column(Enum(Gender), server_default=Gender.NOT_SPECIFIED.name, nullable=True)
    createdAt=Column(TIMESTAMP(timezone=True),
                         nullable=False,
                         server_default=text('now()'))
    updatedAt=Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


@event.listens_for(Users, 'before_update')
def recieve_before_update(mapper, connection, target):
    target.updatedAt= func.now()

class Listing(Base):
    __tablename__="listing"
    id= Column(Integer, primary_key=True, nullable=False)
    type= Column(Enum(Type), nullable=False)
    availableNow= Column(Boolean, server_default="TRUE", nullable=True)
    ownerId= Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    address= Column(String, nullable=False)
    createdAt=Column(TIMESTAMP(timezone=True),
                         nullable=False,
                         server_default=text('now()'))
    updatedAt=Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

@event.listens_for(Listing, 'before_update')
def recieve_before_update(mapper, connection, target):
    target.updatedAt= func.now()