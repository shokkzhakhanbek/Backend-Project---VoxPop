from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse

from app.routers.comments import store
from app.schemas.comment import CommentCategory

router = APIRouter(tags=["ui"])


@router.get("/ui", response_class=HTMLResponse)
def ui_home(
    request: Request,
    page: int = 1,
    limit: int = 10,
    category: str | None = None,
):
    templates = request.app.state.templates

    cat = None
    if category in ("positive", "negative"):
        cat = CommentCategory(category)

    result = store.list(page=page, limit=limit, category=cat)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "page": result["page"],
            "limit": result["limit"],
            "total": result["total"],
            "total_pages": result["total_pages"],
            "category": category,
            "items": result["items"],
        },
    )


@router.post("/ui/comments")
def ui_create_comment(text: str = Form(...), category: str = Form(...)):
    cat = CommentCategory(category)
    store.add(text=text.strip(), category=cat)
    return RedirectResponse(url="/ui", status_code=303)