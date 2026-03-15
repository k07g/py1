import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Query

from src.models import Book, BookCreate, BookListResponse, BookUpdate
from src import database

router = APIRouter(prefix="/books", tags=["books"])


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@router.post("", response_model=Book, status_code=201)
def create_book(body: BookCreate):
    item = {
        "id": str(uuid.uuid4()),
        "created_at": _now(),
        "updated_at": _now(),
        **body.model_dump(exclude_none=True),
    }
    database.put_book(item)
    return item


@router.get("", response_model=BookListResponse)
def list_books(
    limit: int = Query(20, ge=1, le=100),
    last_key: str | None = Query(None),
):
    items, next_key = database.list_books(limit=limit, last_key=last_key)
    return BookListResponse(items=items, count=len(items), last_evaluated_key=next_key)


@router.get("/{book_id}", response_model=Book)
def get_book(book_id: str):
    item = database.get_book(book_id)
    if not item:
        raise HTTPException(status_code=404, detail="Book not found")
    return item


@router.patch("/{book_id}", response_model=Book)
def update_book(book_id: str, body: BookUpdate):
    updates = body.model_dump(exclude_none=True)
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")

    updates["updated_at"] = _now()
    item = database.update_book(book_id, updates)
    if not item:
        raise HTTPException(status_code=404, detail="Book not found")
    return item


@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: str):
    deleted = database.delete_book(book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
