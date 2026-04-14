from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from decimal import Decimal
from typing import Set, Dict, Any, Optional
from app.models import (
    AbstractCustomer,
    BusinessCustomer,
    ResidentialCustomer,
    Order,
    LineItem,
    Product,
    OrderStatus,
)


class CustomerDoesNotExistException(Exception):
    """Raised when a customer is not found."""

    pass


class ProductDoesNotExistException(Exception):
    """Raised when a product is not found."""

    pass


class InvalidQuantityException(Exception):
    """Raised when an invalid quantity is provided."""

    pass


class OrderModifiedException(Exception):
    """Raised when an order has been modified (optimistic locking failure)."""

    pass


class GeneralPersistenceException(Exception):
    """General database exception."""

    pass


class CustomerOrderService:
    """
    Main service for customer order operations.
    Equivalent to Java CustomerOrderServices EJB.
    """

    def __init__(self, db: Session, current_username: str):
        self.db = db
        self.current_username = current_username

    def load_customer(self) -> AbstractCustomer:
        """Load the currently authenticated customer."""
        customer = (
            self.db.query(AbstractCustomer)
            .filter(AbstractCustomer.username == self.current_username)
            .first()
        )
        if not customer:
            raise CustomerDoesNotExistException(
                f"Customer {self.current_username} not found"
            )
        return customer

    def update_address(self, street: str, city: str, state: str, zip_code: str) -> None:
        """Update customer's address."""
        customer = self.load_customer()
        customer.street = street
        customer.city = city
        customer.state = state
        customer.zip_code = zip_code
        self.db.commit()

    def update_info(self, info: Dict[str, Any]) -> None:
        """Update customer type-specific information."""
        customer = self.load_customer()

        if isinstance(customer, BusinessCustomer):
            if "description" in info:
                customer.description = info["description"]
        elif isinstance(customer, ResidentialCustomer):
            if "household_size" in info:
                household_size = info["household_size"]
                if household_size < 1 or household_size > 10:
                    raise ValueError("Household size must be between 1 and 10")
                customer.household_size = household_size

        self.db.commit()

    def add_line_item(
        self, product_id: int, quantity: int, version: Optional[int] = None
    ) -> Order:
        """
        Add a line item to the customer's open order.
        Implements optimistic locking with version checking.
        """
        if quantity <= 0:
            raise InvalidQuantityException("Quantity must be greater than 0")

        customer = self.load_customer()

        # Get or create open order
        if customer.open_order:
            open_order = customer.open_order
            # Check version for optimistic locking
            if version is not None and open_order.version != version:
                raise OrderModifiedException("Order has been modified by another process")
        else:
            open_order = Order(
                customer_id=customer.customer_id,
                status=OrderStatus.OPEN,
                total=Decimal("0.00"),
            )
            self.db.add(open_order)
            self.db.flush()  # Get the order_id
            customer.open_order = open_order

        # Get product
        product = self.db.query(Product).filter(Product.product_id == product_id).first()
        if not product:
            raise ProductDoesNotExistException(f"Product {product_id} not found")

        # Check if line item already exists
        existing_item = (
            self.db.query(LineItem)
            .filter(
                LineItem.order_id == open_order.order_id,
                LineItem.product_id == product_id,
            )
            .first()
        )

        if existing_item:
            # Update existing item
            existing_item.quantity += quantity
            existing_item.amount = product.price * existing_item.quantity
        else:
            # Create new line item
            line_item = LineItem(
                order_id=open_order.order_id,
                product_id=product_id,
                quantity=quantity,
                amount=product.price * quantity,
            )
            self.db.add(line_item)

        # Recalculate order total
        self._recalculate_order_total(open_order)

        # Increment version for optimistic locking
        open_order.version += 1

        self.db.commit()
        self.db.refresh(open_order)
        return open_order

    def remove_line_item(self, product_id: int, version: int) -> Order:
        """Remove a line item from the customer's open order."""
        customer = self.load_customer()

        if not customer.open_order:
            raise CustomerDoesNotExistException("No open order found")

        open_order = customer.open_order

        # Check version for optimistic locking
        if open_order.version != version:
            raise OrderModifiedException("Order has been modified by another process")

        # Find and remove line item
        line_item = (
            self.db.query(LineItem)
            .filter(
                LineItem.order_id == open_order.order_id,
                LineItem.product_id == product_id,
            )
            .first()
        )

        if not line_item:
            raise ProductDoesNotExistException(
                f"Product {product_id} not in order"
            )

        self.db.delete(line_item)

        # Recalculate order total
        self._recalculate_order_total(open_order)

        # Increment version
        open_order.version += 1

        self.db.commit()
        self.db.refresh(open_order)
        return open_order

    def submit(self, version: int) -> None:
        """Submit the customer's open order."""
        customer = self.load_customer()

        if not customer.open_order:
            raise CustomerDoesNotExistException("No open order found")

        open_order = customer.open_order

        # Check version for optimistic locking
        if open_order.version != version:
            raise OrderModifiedException("Order has been modified by another process")

        # Update order status
        open_order.status = OrderStatus.SUBMITTED
        open_order.submit_time = datetime.utcnow()

        # Clear the customer's open order reference
        customer.open_order = None

        self.db.commit()

    def load_customer_history(self) -> Set[Order]:
        """Load all submitted orders for the current customer."""
        customer = self.load_customer()
        orders = (
            self.db.query(Order)
            .filter(
                Order.customer_id == customer.customer_id,
                Order.status != OrderStatus.OPEN,
            )
            .all()
        )
        return set(orders)

    def get_order_history_last_updated_time(self) -> datetime:
        """Get the last update time for customer's order history."""
        customer = self.load_customer()
        latest_order = (
            self.db.query(Order)
            .filter(
                Order.customer_id == customer.customer_id,
                Order.status != OrderStatus.OPEN,
            )
            .order_by(Order.submit_time.desc())
            .first()
        )

        if latest_order and latest_order.submit_time:
            return latest_order.submit_time
        return datetime.utcnow()

    def _recalculate_order_total(self, order: Order) -> None:
        """Recalculate the total for an order based on its line items."""
        total = sum(
            item.amount for item in order.lineitems
        )
        order.total = total
