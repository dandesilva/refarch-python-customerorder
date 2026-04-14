from sqlalchemy.orm import Session
from typing import List
from app.models import Category


class CategoryService:
    """Service for category operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_top_level_categories(self) -> List[Category]:
        """Get all top-level categories (categories without a parent)."""
        return (
            self.db.query(Category).filter(Category.parent_cat_id.is_(None)).all()
        )

    def get_categories_by_parent(self, parent_id: int) -> List[Category]:
        """Get all child categories of a parent category."""
        return (
            self.db.query(Category).filter(Category.parent_cat_id == parent_id).all()
        )

    def get_category(self, category_id: int) -> Category:
        """Get a single category by ID."""
        return self.db.query(Category).filter(Category.cat_id == category_id).first()
