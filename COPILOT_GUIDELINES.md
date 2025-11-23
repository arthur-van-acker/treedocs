# GitHub Copilot Guidelines — Python Project

This file contains coding standards, conventions, and stylistic preferences
for this Python project. Treat it as a “system prompt” for Copilot.

---

## 1. General Principles
- Prioritize **readability and clarity**.
- Keep code **modular** and **well-structured**.
- Prefer **explicit over implicit**.
- Include **type hints** for all functions.
- Avoid overly clever or obfuscated solutions; favor **maintainable, idiomatic Python**.

---

## 2. Naming Conventions
- `snake_case` for variables and functions.
- `PascalCase` for classes.
- Constants in `UPPER_SNAKE_CASE`.
- Use **descriptive names**, avoid single letters except in small loops.

---

## 3. Functions and Methods
- Keep functions **≤ 50 lines** if possible.
- Include **docstrings** describing purpose, parameters, and return type.
- Use **early returns** to reduce nested conditions.
- Validate inputs and handle errors appropriately.

---

## 4. Classes and Modules
- Follow **single responsibility principle**.
- Break large classes into smaller components if needed.
- Include **module-level docstring** describing the purpose of the module.

---

## 5. Formatting and Style
- Follow **PEP8** for formatting.
- Indentation: 4 spaces.
- Line length: max 100 characters.
- Always include a newline at the end of the file.
- Use **single quotes** for strings consistently (`'example'`).

---

## 6. Documentation & Comments
- Use **inline comments** sparingly, only for clarification.
- Include **function-level docstrings** for all public functions.
- Keep comments up-to-date and accurate.

---

## 7. Testing
- Write **unit tests** for new functions/classes.
- Use descriptive test names.
- Prefer **pytest** for testing framework.

---

## 8. Copilot-Specific Notes
- Suggestions should **follow the project conventions above**.
- Prefer **multiline code suggestions** with proper indentation.
- Include **type hints** and **docstrings** in generated code.
- Favor clarity and maintainability over clever tricks.
- Always generate **PEP8-compliant code**.

---

### Example Usage

```python
# Copilot guidelines:
# - snake_case for functions and variables
# - include type hints
# - include docstrings

def calculate_average(numbers: list[float]) -> float:
    """
    Calculate the average of a list of numbers.

    Args:
        numbers (list[float]): List of numeric values.

    Returns:
        float: The average of the numbers.
    """
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)
