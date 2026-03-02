from fastapi import APIRouter, Query

from app.schemas.comment import (
    CommentCreate,
    CommentOut,
    PaginatedComments,
    CommentCategory,
)
from app.storage.comments_store import CommentsStore

router = APIRouter(prefix="/comments", tags=["comments"])

store = CommentsStore()


@router.post("", response_model=CommentOut, status_code=201)
def create_comment(payload: CommentCreate):
    comment = store.add(text=payload.text.strip(), category=payload.category)
    return CommentOut(
        id=comment.id,
        text=comment.text,
        category=comment.category,
        created_at=comment.created_at,
    )


@router.get("", response_model=PaginatedComments)
def list_comments(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    category: CommentCategory | None = Query(None),
):
    result = store.list(page=page, limit=limit, category=category)

    return PaginatedComments(
        page=result["page"],
        limit=result["limit"],
        total=result["total"],
        total_pages=result["total_pages"],
        items=[
            CommentOut(
                id=c.id,
                text=c.text,
                category=c.category,
                created_at=c.created_at,
            )
            for c in result["items"]
        ],
    )