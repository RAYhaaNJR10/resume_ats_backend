from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    DateTime
)

from datetime import datetime

Base = declarative_base()


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    filename = Column(
        String(255)
    )

    name = Column(
        String(255)
    )

    email = Column(
        String(255),
        unique=True
    )

    phone = Column(
        String(50)
    )

    skills = Column(
        Text
    )

    education = Column(
        Text
    )

    experience = Column(
        Text
    )

    linkedin = Column(
        String(500)
    )

    github = Column(
        String(500)
    )

    projects = Column(
        Text
    )

    certifications = Column(
        Text
    )

    ats_score = Column(
        Float,
        default=0
    )

    upload_date = Column(
        DateTime,
        default=datetime.utcnow
    )