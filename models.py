from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text

Base = declarative_base()

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))
    skills = Column(Text)