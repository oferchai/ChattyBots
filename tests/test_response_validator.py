"""
Unit tests for the ResponseValidator.
"""
import pytest

from app.services.response_validator import ResponseValidator

def test_validate_response_valid():
    """Test that a valid response passes validation."""
    validator = ResponseValidator()
    assert validator.validate_response("This is a valid response.") is True

def test_validate_response_empty():
    """Test that an empty response fails validation."""
    validator = ResponseValidator()
    assert validator.validate_response("") is False

def test_validate_response_whitespace_only():
    """Test that a whitespace-only response fails validation."""
    validator = ResponseValidator()
    assert validator.validate_response("   \n\t ") is False

def test_clean_response():
    """Test that clean_response removes leading/trailing whitespace."""
    validator = ResponseValidator()
    cleaned = validator.clean_response("  Hello, World!  \n")
    assert cleaned == "Hello, World!"

def test_clean_response_no_change():
    """Test that clean_response doesn't change already clean strings."""
    validator = ResponseValidator()
    cleaned = validator.clean_response("Hello, World!")
    assert cleaned == "Hello, World!"

