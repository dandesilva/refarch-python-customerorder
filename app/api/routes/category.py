from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional, Union
from app.schemas.category import CategoryResponse, CategoryWithSubcategories
from app.services.category_service import CategoryService
from app.api.deps import get_category_service

router = APIRouter(prefix="/Category", tags=["categories"])


@router.get("", response_model=List[Union[CategoryWithSubcategories, CategoryResponse]])
def get_categories(
    parent_id: Optional[int] = Query(None, alias="parentId"),
    category_service: CategoryService = Depends(get_category_service),
):
    """
    Get categories.
    If parentId is provided, get child categories.
    If parentId is None, get top-level categories with subcategories.
    """
    if parent_id is None:
        # Get top-level categories with their subcategories (for Dojo compatibility)
        top_categories = category_service.get_top_level_categories()
        result = []
        for top_cat in top_categories:
            sub_cats = category_service.get_categories_by_parent(top_cat.cat_id)
            cat_dict = {
                "cat_id": top_cat.cat_id,
                "id": top_cat.cat_id,
                "name": top_cat.name,
                "parent_cat_id": top_cat.parent_cat_id,
                "subCategories": [
                    {
                        "cat_id": sub.cat_id,
                        "id": sub.cat_id,
                        "name": sub.name,
                        "parent_cat_id": sub.parent_cat_id
                    }
                    for sub in sub_cats
                ] if sub_cats else None
            }
            result.append(CategoryWithSubcategories(**cat_dict))
        return result
    else:
        categories = category_service.get_categories_by_parent(parent_id)
        return [CategoryResponse.model_validate(cat) for cat in categories]


@router.get("/{id}", response_model=CategoryResponse)
def get_category(
    id: int,
    category_service: CategoryService = Depends(get_category_service),
):
    """Get a single category by ID."""
    category = category_service.get_category(id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category
