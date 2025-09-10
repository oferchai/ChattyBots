# Gemini Coding Style

This document outlines the coding style for the project, as understood by the Gemini agent.

## Python

*   **Style Guide:** PEP 8
*   **Formatter:** Black (line length: 88 characters)
*   **Naming Conventions:**
    *   `snake_case` for variables, functions, and filenames.
    *   `PascalCase` for classes.
    *   `SCREAMING_SNAKE_CASE` for constants.
*   **Docstrings:** PEP 257, with detailed docstrings for modules, classes, and functions.
*   **Type Hinting:** PEP 484, mandatory for all function and method signatures.
*   **Imports:** Organized into three sections: standard library, third-party, and local application.

## Testing

*   **Framework:** pytest
*   **File Naming:** `test_*.py`
*   **Test Naming:** `test_*`
*   **Fixtures:** Used for setting up test conditions.
*   **Mocks:** `unittest.mock` is used for mocking objects and functions.

## Error Handling

*   A custom exception hierarchy is used, with a base `ChatbotError` class.
*   Structured logging is used to log errors with context.

## Project Structure

*   The project is organized into `backend`, `frontend`, `tests`, and `data` directories.
*   The backend follows a modular structure, with clear separation of concerns.
