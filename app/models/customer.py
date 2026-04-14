from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class AbstractCustomer(Base):
    """
    Base customer model using single table inheritance.
    Equivalent to JPA AbstractCustomer with SINGLE_TABLE inheritance strategy.
    """

    __tablename__ = "customer"

    customer_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), nullable=False, unique=True, index=True)
    name = Column(String(30), nullable=False)
    type = Column(String(20), nullable=False)  # Discriminator column

    # Address fields (embedded)
    street = Column(String(100))
    city = Column(String(50))
    state = Column(String(2))
    zip_code = Column(String(10))

    # Relationships
    open_order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=True)
    open_order = relationship(
        "Order",
        foreign_keys=[open_order_id],
        post_update=True,
        uselist=False,
    )
    orders = relationship(
        "Order",
        back_populates="customer",
        foreign_keys="Order.customer_id",
        lazy="dynamic",
    )

    # Polymorphic configuration
    __mapper_args__ = {
        "polymorphic_identity": "abstract",
        "polymorphic_on": type,
        "with_polymorphic": "*",
    }

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.customer_id}, username={self.username})>"


class BusinessCustomer(AbstractCustomer):
    """
    Business customer with additional business-specific fields.
    """

    description = Column(String(500))
    business_partner = Column(String(100))
    volume_discount = Column(String(10))

    __mapper_args__ = {
        "polymorphic_identity": "business",
    }


class ResidentialCustomer(AbstractCustomer):
    """
    Residential customer with household-specific fields.
    """

    frequent_customer = Column(String(10))
    household_size = Column(Integer)

    __mapper_args__ = {
        "polymorphic_identity": "residential",
    }
