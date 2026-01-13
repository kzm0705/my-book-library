from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from enum import Enum

class BookStatus(str, Enum):
    WISH = "読みたい"
    READING = "読書中"
    COMPLETED = "読了"


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="本のタイトル")
    title_kana: Optional[str] = None
    author: str = Field(..., min_length=1, max_length=50, description="著者名")
    status: BookStatus = Field(default=BookStatus.WISH, description="読書状態")
    read_date: Optional[date] = Field(None, description="読み終えた日")
    memo: Optional[str] = Field(None, max_length=500, description="感想メモ")

# 本を登録する時の形
class BookCreate(BookBase):
    pass


# データを返す時の形（IDなどを含める）
class Book(BookBase):
    id: int

    class Config:
        from_attributes = True


class BookUpdate(BookBase):
    title : Optional[str] = Field(None, min_length=1, max_length=100, description="本のタイトル")
    title_kana: Optional[str] = None
    author : Optional[str] = Field(None, min_length=1, max_length=50, description="著者名")
    status: Optional[BookStatus] = None
    read_date: Optional[date] = Field(None, description="読み終えた日")
    memo: Optional[str] = Field(None, max_length=500, description="感想メモ")


class SortBase(BaseModel):
    sort_by : Optional[str] = None
