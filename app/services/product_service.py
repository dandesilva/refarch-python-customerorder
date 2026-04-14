from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from app.models import Product, Category
from app.models.category import product_category


class ProductDoesNotExistException(Exception):
    """Raised when a product is not found."""

    pass


class ProductSearchService:
    """
    Service for product search and retrieval operations.
    Equivalent to Java ProductSearchService EJB.
    """

    def __init__(self, db: Session):
        self.db = db

    def load_product(self, product_id: int) -> Product:
        """Load a single product by ID."""
        product = self.db.query(Product).filter(Product.product_id == product_id).first()
        if not product:
            raise ProductDoesNotExistException(f"Product with ID {product_id} not found")
        return product

    def load_products_by_category(self, category_id: int) -> List[Product]:
        """
        Load all products in a category or its subcategories.
        Implements the native query from the Java version.
        """
        # Native SQL query matching the Java @NamedNativeQuery
        query = text(
            """
            SELECT DISTINCT p.product_id, p.name, p.price, p.description, p.image
            FROM product AS p, prod_cat AS pc, category AS c
            WHERE (c.cat_id = :cat_id OR c.parent_cat_id = :cat_id)
              AND pc.cat_id = c.cat_id
              AND pc.product_id = p.product_id
            """
        )

        result = self.db.execute(query, {"cat_id": category_id})
        rows = result.fetchall()

        # Convert to Product objects
        products = []
        for row in rows:
            product = Product(
                product_id=row[0],
                name=row[1],
                price=row[2],
                description=row[3],
                image=row[4],
            )
            products.append(product)

        return products

    def search_products(self, search_term: Optional[str] = None) -> List[Product]:
        """Search products by name."""
        query = self.db.query(Product)
        if search_term:
            query = query.filter(Product.name.ilike(f"%{search_term}%"))
        return query.all()
