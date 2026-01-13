from .database import Base
from sqlalchemy import Column, Integer, String, Date

class Books(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    title_kana = Column(String)
    author = Column(String)
    status = Column(String, default="読みたい")
    read_date = Column(Date, nullable=True)
    memo = Column(String, nullable=True)