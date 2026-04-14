from sqlalchemy import Column, Integer, String, Numeric, text
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.category import product_category


class Product(Base):
    """
    Product model representing items available for purchase.
    """

    __tablename__ = "product"

    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    description = Column(String(500))
    image = Column(String(200))  # Image path

    # Relationship with categories (many-to-many)
    categories = relationship(
        "Category",
        secondary=product_category,
        back_populates="products",
        lazy="joined",
    )

    def __repr__(self):
        return f"<Product(id={self.product_id}, name={self.name}, price={self.price})>"
