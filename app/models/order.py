from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    DateTime,
    ForeignKey,
    Enum as SQLEnum,
    BigInteger,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from enum import Enum
from app.database import Base


class OrderStatus(str, Enum):
    """Order status enumeration matching the Java enum."""

    OPEN = "OPEN"
    SUBMITTED = "SUBMITTED"
    SHIPPED = "SHIPPED"
    CLOSED = "CLOSED"


class Order(Base):
    """
    Customer order containing line items.
    """

    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    total = Column(Numeric(10, 2), default=0)
    status = Column(SQLEnum(OrderStatus), nullable=False, default=OrderStatus.OPEN)
    submit_time = Column(DateTime, nullable=True)
    version = Column(BigInteger, nullable=False, default=0)  # For optimistic locking

    # Foreign key to customer
    customer_id = Column(Integer, ForeignKey("customer.customer_id"), nullable=False)

    # Relationships
    customer = relationship(
        "AbstractCustomer",
        back_populates="orders",
        foreign_keys=[customer_id],
    )
    lineitems = relationship(
        "LineItem",
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="joined",
    )

    def __repr__(self):
        return f"<Order(id={self.order_id}, status={self.status}, total={self.total})>"


class LineItem(Base):
    """
    Individual item in an order with quantity and calculated amount.
    """

    __tablename__ = "line_item"

    # Composite primary key
    order_id = Column(Integer, ForeignKey("orders.order_id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("product.product_id"), primary_key=True)

    quantity = Column(Integer, nullable=False, default=1)
    amount = Column(Numeric(10, 2), nullable=False)
    version = Column(BigInteger, nullable=False, default=0)  # For optimistic locking

    # Relationships
    order = relationship("Order", back_populates="lineitems")
    product = relationship("Product")

    def __repr__(self):
        return f"<LineItem(order_id={self.order_id}, product_id={self.product_id}, qty={self.quantity})>"
