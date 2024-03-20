from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Beer(Base):
    __tablename__ = "beer"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    alcohol_content = Column(Float)
    flavor = Column(String)
    packing = Column(String)
    user_rating = Column(Float)
    region = Column(String)
    season = Column(String)
