"""Shared pytest fixtures for application testing."""

import pytest
from app import app  # This imports the Flask app for testing

@pytest.fixture
def client():
    """Provide a Flask test client for route tests."""
    with app.test_client() as test_client:
        yield test_client
