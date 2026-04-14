"""API dependencies."""

from typing import Generator
from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_username
from app.services import CustomerOrderService, ProductSearchService, CategoryService


def get_customer_service(
    db: Session = Depends(get_db),
    current_username: str = Depends(get_current_username),
) -> CustomerOrderService:
    """Dependency for getting CustomerOrderService."""
    return CustomerOrderService(db, current_username)


def get_product_service(db: Session = Depends(get_db)) -> ProductSearchService:
    """Dependency for getting ProductSearchService."""
    return ProductSearchService(db)


def get_category_service(db: Session = Depends(get_db)) -> CategoryService:
    """Dependency for getting CategoryService."""
    return CategoryService(db)


def get_etag_version(if_match: str | None = Header(None)) -> int | None:
    """Extract version from If-Match header (ETag) for optimistic locking."""
    if if_match:
        try:
            return int(if_match.strip('"'))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid If-Match header")
    return None


def get_if_modified_since(
    if_modified_since: str | None = Header(None)
) -> str | None:
    """Extract If-Modified-Since header for conditional requests."""
    return if_modified_since
