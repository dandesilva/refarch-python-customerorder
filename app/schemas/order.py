from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime
from typing import List, Optional
from app.models.order import OrderStatus


class LineItemResponse(BaseModel):
    """Line item in an order."""

    product_id: int
    quantity: int
    amount: Decimal

    class Config:
        from_attributes = True


class LineItemCreate(BaseModel):
    """Schema for creating a line item."""

    product_id: int = Field(..., alias="productId")
    quantity: int = Field(1, ge=1)
    version: Optional[int] = None

    class Config:
        populate_by_name = True


class OrderResponse(BaseModel):
    """Order response schema."""

    order_id: int
    total: Decimal
    status: OrderStatus
    submit_time: Optional[datetime] = None
    version: int
    lineitems: List[LineItemResponse] = []

    class Config:
        from_attributes = True


class OrderHistoryResponse(BaseModel):
    """Order history response."""

    orders: List[OrderResponse]
    last_modified: Optional[datetime] = None
