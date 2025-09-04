"""
Prompt Manager for the Multi-Agent AI Chat System.

This module handles prompt templating and dynamic prompt injection.
"""
from typing import Dict, Any

class PromptManager:
    """Manages prompt templates and dynamic prompt injection."""

    def __init__(self, templates: Dict[str, str] = None):
        self.templates = templates or {}

    def get_prompt(self, template_name: str, **kwargs) -> str:
        """Retrieves and formats a prompt from a template."""
        template = self.templates.get(template_name)
        if not template:
            raise ValueError(f"Prompt template '{template_name}' not found.")
        return template.format(**kwargs)

    def add_template(self, template_name: str, template_string: str):
        """Adds or updates a prompt template."""
        self.templates[template_name] = template_string
