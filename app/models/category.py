from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

# Association table for many-to-many relationship between Product and Category
product_category = Table(
    "prod_cat",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("product.product_id"), primary_key=True),
    Column("cat_id", Integer, ForeignKey("category.cat_id"), primary_key=True),
)


class Category(Base):
    """
    Product category with hierarchical parent-child relationships.
    """

    __tablename__ = "category"

    cat_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    parent_cat_id = Column(Integer, ForeignKey("category.cat_id"), nullable=True)

    # Self-referential relationship for hierarchy
    parent = relationship("Category", remote_side=[cat_id], backref="children")

    # Relationship with products
    products = relationship(
        "Product",
        secondary=product_category,
        back_populates="categories",
    )

    def __repr__(self):
        return f"<Category(id={self.cat_id}, name={self.name})>"
