from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional

from app.schemas.comment import CommentCategory


@dataclass
class Comment:
    id: int
    text: str
    category: CommentCategory
    created_at: datetime


class CommentsStore:
    def __init__(self):
        self._comments: List[Comment] = []
        self._next_id: int = 1

    def add(self, text: str, category: CommentCategory) -> Comment:
        comment = Comment(
            id=self._next_id,
            text=text,
            category=category,
            created_at=datetime.now(timezone.utc),
        )
        self._next_id += 1

        self._comments.insert(0, comment)
        return comment

    def list(
        self,
        page: int = 1,
        limit: int = 10,
        category: Optional[CommentCategory] = None,
    ):
        if page < 1:
            page = 1
        if limit < 1:
            limit = 10
        if limit > 50:
            limit = 50

        data = self._comments
        if category is not None:
            data = [c for c in data if c.category == category]

        total = len(data)
        start = (page - 1) * limit
        end = start + limit
        items = data[start:end]

        total_pages = (total + limit - 1) // limit if total > 0 else 1

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages,
            "items": items,
        }