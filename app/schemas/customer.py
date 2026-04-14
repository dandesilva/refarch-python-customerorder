from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.order import OrderResponse


class AddressBase(BaseModel):
    """Address embedded in customer."""

    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = Field(None, max_length=2)
    zip_code: Optional[str] = Field(None, max_length=10)


class AddressUpdate(AddressBase):
    """Schema for updating customer address."""

    pass


class CustomerBase(BaseModel):
    """Base customer schema."""

    name: str
    type: str

    class Config:
        from_attributes = True


class CustomerResponse(CustomerBase):
    """Customer response schema."""

    customer_id: int
    username: str
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    open_order: Optional[OrderResponse] = None

    # Business customer fields
    description: Optional[str] = None
    business_partner: Optional[str] = None
    volume_discount: Optional[str] = None

    # Residential customer fields
    frequent_customer: Optional[str] = None
    household_size: Optional[int] = None

    class Config:
        from_attributes = True


class CustomerInfoUpdate(BaseModel):
    """Schema for updating customer info (type-specific fields)."""

    # For business customers
    description: Optional[str] = None

    # For residential customers
    household_size: Optional[int] = Field(None, ge=1, le=10)
