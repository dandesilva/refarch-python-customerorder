from fastapi import APIRouter, Depends, HTTPException, Response
from typing import List
from datetime import datetime, timedelta
from app.schemas.product import ProductResponse
from app.services.product_service import (
    ProductSearchService,
    ProductDoesNotExistException,
)
from app.api.deps import get_product_service

router = APIRouter(prefix="/Product", tags=["products"])


@router.get("/{id}", response_model=ProductResponse)
def get_product(
    id: int,
    response: Response,
    product_service: ProductSearchService = Depends(get_product_service),
):
    """
    Get a single product by ID.
    Sets Expires header for caching (24 hours).
    """
    try:
        product = product_service.load_product(id)

        # Set cache expiration to midnight tomorrow (matching Java implementation)
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
        response.headers["Expires"] = tomorrow.strftime("%a, %d %b %Y %H:%M:%S GMT")

        return ProductResponse.from_orm(product)
    except ProductDoesNotExistException:
        raise HTTPException(status_code=404, detail="Product not found")


@router.get("", response_model=List[ProductResponse])
@router.get("/", response_model=List[ProductResponse])
def get_products_by_category(
    categoryId: int,
    product_service: ProductSearchService = Depends(get_product_service),
):
    """
    Get all products in a category or its subcategories.
    Query parameter: categoryId
    """
    if categoryId <= 0:
        raise HTTPException(status_code=400, detail="Invalid category ID")

    products = product_service.load_products_by_category(categoryId)
    return [ProductResponse.from_orm(p) for p in products]
