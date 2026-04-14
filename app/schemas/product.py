from pydantic import BaseModel, Field
from decimal import Decimal
from typing import List


class ProductResponse(BaseModel):
    """Product response schema."""

    product_id: int
    id: int = None  # For Dojo compatibility
    name: str
    price: str  # String for Dojo compatibility
    description: str | None = None
    image: str | None = None

    class Config:
        from_attributes = True
        populate_by_name = True

    @classmethod
    def from_orm(cls, obj):
        """Custom from_orm to handle price conversion and id field."""
        data = {
            'product_id': obj.product_id,
            'id': obj.product_id,
            'name': obj.name,
            'price': str(obj.price),
            'description': obj.description,
            'image': obj.image
        }
        return cls(**data)


class ProductList(BaseModel):
    """List of products response."""

    products: List[ProductResponse]
