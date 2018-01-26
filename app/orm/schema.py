from sqlalchemy import *
from engine import engine
from sqlalchemy.ext.declarative import declarative_base

meta = MetaData(bind=engine)

Base = declarative_base(engine)

"""
    ORM SCHEMA LOAD FROM DATABASE
"""
class WebStore(Base):
    __tablename__ = 'WebStored'
    __table_args__ = { 'autoload': True }

class WebAgent(Base):
    __tablename__ = 'WebAgent'
    __table_args__ = { 'autoload': True }

