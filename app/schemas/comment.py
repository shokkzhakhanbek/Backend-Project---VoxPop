from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field


class CommentCategory(str, Enum):
    positive = "positive"
    negative = "negative"


class CommentCreate(BaseModel):
    text: str = Field(..., min_length=1, max_length=500)
    category: CommentCategory


class CommentOut(BaseModel):
    id: int
    text: str
    category: CommentCategory
    created_at: datetime


class PaginatedComments(BaseModel):
    page: int
    limit: int
    total: int
    total_pages: int
    items: list[CommentOut]