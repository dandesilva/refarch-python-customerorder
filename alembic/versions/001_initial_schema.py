"""Initial schema and seed data

Revision ID: 001
Revises:
Create Date: 2026-04-13

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create tables

    # Category table
    op.create_table(
        'category',
        sa.Column('cat_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('parent_cat_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['parent_cat_id'], ['category.cat_id'], ),
        sa.PrimaryKeyConstraint('cat_id')
    )
    op.create_index(op.f('ix_category_cat_id'), 'category', ['cat_id'], unique=False)

    # Product table
    op.create_table(
        'product',
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('description', sa.String(length=500), nullable=True),
        sa.Column('image', sa.String(length=200), nullable=True),
        sa.PrimaryKeyConstraint('product_id')
    )
    op.create_index(op.f('ix_product_product_id'), 'product', ['product_id'], unique=False)

    # Product-Category association table
    op.create_table(
        'prod_cat',
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('cat_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['cat_id'], ['category.cat_id'], ),
        sa.ForeignKeyConstraint(['product_id'], ['product.product_id'], ),
        sa.PrimaryKeyConstraint('product_id', 'cat_id')
    )

    # Customer table
    op.create_table(
        'customer',
        sa.Column('customer_id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=30), nullable=False),
        sa.Column('name', sa.String(length=30), nullable=False),
        sa.Column('type', sa.String(length=20), nullable=False),
        sa.Column('street', sa.String(length=100), nullable=True),
        sa.Column('city', sa.String(length=50), nullable=True),
        sa.Column('state', sa.String(length=2), nullable=True),
        sa.Column('zip_code', sa.String(length=10), nullable=True),
        sa.Column('open_order_id', sa.Integer(), nullable=True),
        sa.Column('description', sa.String(length=500), nullable=True),
        sa.Column('business_partner', sa.String(length=100), nullable=True),
        sa.Column('volume_discount', sa.String(length=10), nullable=True),
        sa.Column('frequent_customer', sa.String(length=10), nullable=True),
        sa.Column('household_size', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('customer_id')
    )
    op.create_index(op.f('ix_customer_customer_id'), 'customer', ['customer_id'], unique=False)
    op.create_index(op.f('ix_customer_username'), 'customer', ['username'], unique=True)

    # Orders table
    op.create_table(
        'orders',
        sa.Column('order_id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('total', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('status', sa.Enum('OPEN', 'SUBMITTED', 'SHIPPED', 'CLOSED', name='orderstatus'), nullable=False),
        sa.Column('submit_time', sa.DateTime(), nullable=True),
        sa.Column('version', sa.BigInteger(), nullable=False),
        sa.Column('customer_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['customer_id'], ['customer.customer_id'], ),
        sa.PrimaryKeyConstraint('order_id')
    )
    op.create_index(op.f('ix_orders_order_id'), 'orders', ['order_id'], unique=False)

    # Add foreign key for open_order_id in customer table
    op.create_foreign_key('fk_customer_open_order', 'customer', 'orders', ['open_order_id'], ['order_id'])

    # LineItem table
    op.create_table(
        'line_item',
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('version', sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(['order_id'], ['orders.order_id'], ),
        sa.ForeignKeyConstraint(['product_id'], ['product.product_id'], ),
        sa.PrimaryKeyConstraint('order_id', 'product_id')
    )

    # Insert seed data

    # Categories
    categories = [
        (1, 'Electronics', None),
        (2, 'Computers', 1),
        (3, 'Laptops', 2),
        (4, 'Desktops', 2),
        (5, 'Home & Garden', None),
        (6, 'Furniture', 5),
        (7, 'Appliances', 5),
        (8, 'Entertainment', None),
        (9, 'Gaming', 8),
        (10, 'Movies', 8),
    ]

    for cat_id, name, parent_id in categories:
        if parent_id:
            op.execute(f"""
                INSERT INTO category (cat_id, name, parent_cat_id)
                VALUES ({cat_id}, '{name}', {parent_id})
            """)
        else:
            op.execute(f"""
                INSERT INTO category (cat_id, name, parent_cat_id)
                VALUES ({cat_id}, '{name}', NULL)
            """)

    # Products
    products = [
        (1, 'Sony Smartphone', 299.99, 'High-performance smartphone with 5G', '/images/SonyPhone.jpg'),
        (2, 'BlackBerry Classic', 199.99, 'Business smartphone with physical keyboard', '/images/BlackBerry.jpg'),
        (3, 'PlayStation 3', 399.99, 'Gaming console with Blu-ray player', '/images/PS3.jpg'),
        (4, 'Xbox 360', 349.99, 'Microsoft gaming console', '/images/xbox360.jpg'),
        (5, 'Nintendo Wii', 299.99, 'Family-friendly gaming console', '/images/wii.jpg'),
        (6, 'Sony LED TV', 899.99, '55-inch 4K Ultra HD Smart TV', '/images/SonyTV.jpg'),
        (7, 'The Empire Strikes Back', 19.99, 'Star Wars Episode V on Blu-ray', '/images/Empire.jpg'),
        (8, 'A New Hope', 19.99, 'Star Wars Episode IV on Blu-ray', '/images/NewHope.jpg'),
        (9, 'Return of the Jedi', 19.99, 'Star Wars Episode VI on Blu-ray', '/images/Return.jpg'),
        (10, 'Superstar Concert DVD', 14.99, 'Live concert recording', '/images/Superstar.jpg'),
    ]

    for prod_id, name, price, desc, image in products:
        image_value = f"'{image}'" if image else 'NULL'
        op.execute(f"""
            INSERT INTO product (product_id, name, price, description, image)
            VALUES ({prod_id}, '{name}', {price}, '{desc}', {image_value})
        """)

    # Product-Category associations
    product_categories = [
        (1, 2),  # Sony Smartphone -> Computers
        (2, 2),  # BlackBerry -> Computers
        (3, 9),  # PS3 -> Gaming
        (4, 9),  # Xbox 360 -> Gaming
        (5, 9),  # Wii -> Gaming
        (6, 1),  # Sony TV -> Electronics
        (7, 10), # Empire -> Movies
        (8, 10), # New Hope -> Movies
        (9, 10), # Return -> Movies
        (10, 10), # Superstar -> Movies
    ]

    for product_id, cat_id in product_categories:
        op.execute(f"""
            INSERT INTO prod_cat (product_id, cat_id)
            VALUES ({product_id}, {cat_id})
        """)

    # Customers
    op.execute("""
        INSERT INTO customer (customer_id, username, name, type, street, city, state, zip_code,
                              frequent_customer, household_size, open_order_id)
        VALUES (1, 'rbarcia', 'Rosco P. Coltrane', 'residential', '10 Farm Road',
                'Hazzard', 'GA', '31522', 'Y', 4, NULL)
    """)

    op.execute("""
        INSERT INTO customer (customer_id, username, name, type, street, city, state, zip_code,
                              description, business_partner, volume_discount, open_order_id)
        VALUES (2, 'bcorporate', 'Big Corporation', 'business', '100 Business Blvd',
                'Atlanta', 'GA', '30301', 'Large enterprise customer', 'Y', '10', NULL)
    """)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('line_item')
    op.drop_constraint('fk_customer_open_order', 'customer', type_='foreignkey')
    op.drop_index(op.f('ix_orders_order_id'), table_name='orders')
    op.drop_table('orders')
    op.drop_index(op.f('ix_customer_username'), table_name='customer')
    op.drop_index(op.f('ix_customer_customer_id'), table_name='customer')
    op.drop_table('customer')
    op.drop_table('prod_cat')
    op.drop_index(op.f('ix_product_product_id'), table_name='product')
    op.drop_table('product')
    op.drop_index(op.f('ix_category_cat_id'), table_name='category')
    op.drop_table('category')

