from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    status = Column(String, default="pending")
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)