"""API endpoint tests."""

import pytest
from fastapi import status


class TestHealthCheck:
    """Test health check endpoints."""

    def test_root(self, client):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "status" in data

    def test_health(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"


class TestProductAPI:
    """Test product endpoints."""

    def test_get_products_by_category_invalid(self, client):
        """Test getting products with invalid category ID."""
        response = client.get("/api/v1/Product?categoryId=0")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_product_not_found(self, client):
        """Test getting non-existent product."""
        response = client.get("/api/v1/Product/99999")
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestCategoryAPI:
    """Test category endpoints."""

    def test_get_categories(self, client):
        """Test getting top-level categories."""
        response = client.get("/api/v1/Category")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)


# Add more tests as needed for authentication, customer operations, etc.
