"""
Unit tests for the PromptManager.
"""
import pytest

from app.services.prompt_manager import PromptManager

def test_prompt_manager_initialization():
    """Test that the PromptManager can be initialized."""
    manager = PromptManager()
    assert manager.templates == {}

def test_add_template():
    """Test that a template can be added and retrieved."""
    manager = PromptManager()
    manager.add_template("greeting", "Hello, {name}!")
    assert manager.templates["greeting"] == "Hello, {name}!"

def test_get_prompt_success():
    """Test that a prompt can be retrieved and formatted correctly."""
    manager = PromptManager()
    manager.add_template("greeting", "Hello, {name}!")
    prompt = manager.get_prompt("greeting", name="World")
    assert prompt == "Hello, World!"

def test_get_prompt_not_found():
    """Test that getting a non-existent prompt raises an error."""
    manager = PromptManager()
    with pytest.raises(ValueError, match="Prompt template 'non_existent' not found."):
        manager.get_prompt("non_existent")

def test_add_template_overwrite():
    """Test that adding a template with an existing name overwrites it."""
    manager = PromptManager()
    manager.add_template("test", "Initial template.")
    manager.add_template("test", "Updated template.")
    assert manager.templates["test"] == "Updated template."
