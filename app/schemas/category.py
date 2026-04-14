from pydantic import BaseModel, Field
from typing import Optional, List


class CategoryResponse(BaseModel):
    """Category response schema."""

    cat_id: int
    id: int = None  # Alias for Dojo compatibility
    name: str
    parent_cat_id: Optional[int] = None

    class Config:
        from_attributes = True

    def __init__(self, **data):
        super().__init__(**data)
        # Set id to cat_id for Dojo compatibility
        if self.id is None:
            self.id = self.cat_id


class CategoryWithSubcategories(BaseModel):
    """Category with subcategories for Dojo frontend."""

    cat_id: int
    id: int = None
    name: str
    parent_cat_id: Optional[int] = None
    subCategories: Optional[List[CategoryResponse]] = None

    class Config:
        from_attributes = True

    def __init__(self, **data):
        super().__init__(**data)
        if self.id is None:
            self.id = self.cat_id


class CategoryListResponse(BaseModel):
    """List of categories."""

    categories: List[CategoryResponse]
