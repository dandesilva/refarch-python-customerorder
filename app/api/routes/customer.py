from fastapi import APIRouter, Depends, HTTPException, Response, Header
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.schemas.customer import (
    CustomerResponse,
    AddressUpdate,
    CustomerInfoUpdate,
)
from app.schemas.order import (
    OrderResponse,
    LineItemCreate,
    OrderHistoryResponse,
)
from app.services.customer_service import (
    CustomerOrderService,
    CustomerDoesNotExistException,
    ProductDoesNotExistException,
    InvalidQuantityException,
    OrderModifiedException,
)
from app.api.deps import get_customer_service, get_etag_version

router = APIRouter(prefix="/Customer", tags=["customers"])


@router.get("", response_model=CustomerResponse)
def get_customer(
    response: Response,
    customer_service: CustomerOrderService = Depends(get_customer_service),
):
    """
    Get the current customer's information.
    Sets ETag header if customer has an open order.
    """
    try:
        customer = customer_service.load_customer()
        if customer.open_order:
            response.headers["ETag"] = str(customer.open_order.version)
        return customer
    except CustomerDoesNotExistException:
        raise HTTPException(status_code=404, detail="Customer not found")


@router.put("/Address", status_code=204)
def update_address(
    address: AddressUpdate,
    customer_service: CustomerOrderService = Depends(get_customer_service),
):
    """Update the customer's address."""
    try:
        customer_service.update_address(
            street=address.street or "",
            city=address.city or "",
            state=address.state or "",
            zip_code=address.zip_code or "",
        )
        return Response(status_code=204)
    except CustomerDoesNotExistException:
        raise HTTPException(status_code=404, detail="Customer not found")


@router.post("/Info", status_code=204)
def update_info(
    info: CustomerInfoUpdate,
    customer_service: CustomerOrderService = Depends(get_customer_service),
):
    """Update customer type-specific information."""
    try:
        info_dict = info.model_dump(exclude_none=True)
        customer_service.update_info(info_dict)
        return Response(status_code=204)
    except CustomerDoesNotExistException:
        raise HTTPException(status_code=404, detail="Customer not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/OpenOrder/LineItem", response_model=OrderResponse)
def add_line_item(
    line_item: LineItemCreate,
    response: Response,
    customer_service: CustomerOrderService = Depends(get_customer_service),
    version: Optional[int] = Depends(get_etag_version),
):
    """
    Add a line item to the customer's open order.
    Uses If-Match header for optimistic locking.
    """
    try:
        order = customer_service.add_line_item(
            product_id=line_item.product_id,
            quantity=line_item.quantity,
            version=version or line_item.version,
        )
        response.headers["ETag"] = str(order.version)
        response.headers["Location"] = "/Customer"
        return order
    except CustomerDoesNotExistException:
        raise HTTPException(status_code=404, detail="Customer not found")
    except ProductDoesNotExistException:
        raise HTTPException(status_code=404, detail="Product not found")
    except InvalidQuantityException:
        raise HTTPException(status_code=400, detail="Invalid quantity")
    except OrderModifiedException:
        raise HTTPException(
            status_code=412, detail="Order has been modified"
        )


@router.delete("/OpenOrder/LineItem/{product_id}", response_model=OrderResponse)
def remove_line_item(
    product_id: int,
    response: Response,
    customer_service: CustomerOrderService = Depends(get_customer_service),
    version: Optional[int] = Depends(get_etag_version),
):
    """
    Remove a line item from the customer's open order.
    Requires If-Match header for optimistic locking.
    """
    if version is None:
        raise HTTPException(
            status_code=412, detail="If-Match header required"
        )

    try:
        order = customer_service.remove_line_item(product_id, version)
        response.headers["ETag"] = str(order.version)
        return order
    except CustomerDoesNotExistException:
        raise HTTPException(status_code=404, detail="Customer not found")
    except ProductDoesNotExistException:
        raise HTTPException(status_code=404, detail="Product not in order")
    except OrderModifiedException:
        raise HTTPException(
            status_code=412, detail="Order has been modified"
        )


@router.post("/OpenOrder", status_code=204)
def submit_order(
    customer_service: CustomerOrderService = Depends(get_customer_service),
    version: Optional[int] = Depends(get_etag_version),
):
    """
    Submit the customer's open order.
    Requires If-Match header for optimistic locking.
    """
    if version is None:
        raise HTTPException(
            status_code=412, detail="If-Match header required"
        )

    try:
        customer_service.submit(version)
        return Response(status_code=204)
    except CustomerDoesNotExistException:
        raise HTTPException(status_code=404, detail="Customer not found")
    except OrderModifiedException:
        raise HTTPException(
            status_code=412, detail="Order has been modified"
        )


@router.get("/Orders", response_model=List[OrderResponse])
def get_order_history(
    response: Response,
    if_modified_since: Optional[str] = Header(None, alias="If-Modified-Since"),
    customer_service: CustomerOrderService = Depends(get_customer_service),
):
    """
    Get customer's order history.
    Supports conditional requests with If-Modified-Since header.
    """
    try:
        last_modified = customer_service.get_order_history_last_updated_time()

        # Check if-modified-since header
        if if_modified_since:
            try:
                header_date = datetime.strptime(
                    if_modified_since, "%Y-%m-%d %H:%M:%S.%f"
                )
                if header_date >= last_modified:
                    return Response(status_code=304)  # Not Modified
            except ValueError:
                pass  # Invalid date format, ignore

        orders = customer_service.load_customer_history()
        response.headers["Last-Modified"] = last_modified.strftime(
            "%Y-%m-%d %H:%M:%S.%f"
        )
        return list(orders)

    except CustomerDoesNotExistException:
        raise HTTPException(status_code=404, detail="Customer not found")
