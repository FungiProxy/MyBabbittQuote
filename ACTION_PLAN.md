# Project Action Plan

_Last updated: {{DATE}}_

## Overview
This file contains the current prioritized action plan for the MyBabbittQuote project. It is intended to help new contributors and AI agents quickly understand the project's status, priorities, and next steps. Please update this file as progress is made or priorities change.

---

## Project State
- **Core business logic:** Implemented (pricing, quoting, models)
- **UI:** Functional, but large files and some missing features
- **Testing:** Present, but needs centralization and more coverage
- **Documentation:** Needs improvement
- **Export:** Basic structure present, needs full implementation

---

## Prioritized Action Plan

### 1. Documentation & Onboarding
- [ ] Expand `README.md` with project overview, setup, usage, and testing instructions
- [ ] Add docstrings to all public classes, methods, and complex functions
- [ ] Document environment setup and dependencies

### 2. Testing & Quality Assurance
- [ ] Move all test scripts to the `tests/` directory and use consistent naming (`test_*.py`)
- [ ] Increase unit test coverage for business logic (pricing, quote creation, option compatibility)
- [ ] Add UI tests for critical workflows (consider `pytest-qt` or `pytest-pyside6`)
- [ ] Use fixtures/mocks to isolate tests from production data

### 3. Code Organization & Refactoring
- [ ] Refactor large UI files into smaller, focused components or widgets
- [ ] Consider using service classes (not just static methods) for extensibility
- [ ] Ensure all subdirectories have `__init__.py` for explicit package structure

### 4. Security & Input Validation
- [ ] Add input validation for all user inputs (UI forms, file uploads, etc.)
- [ ] Replace `print` statements with proper logging and user-friendly error messages
- [ ] Use environment variables for secrets and sensitive settings

### 5. Business Logic Improvements
- [ ] Move hardcoded pricing rules to configuration files or database tables
- [ ] Add business rule validation (e.g., valid product/material combinations)
- [ ] Optimize database access (profile for N+1 queries, use eager loading, cache expensive lookups)

### 6. Dependency & Build Management
- [ ] Pin dependency versions more strictly in `requirements.txt`
- [ ] Consider using `pip-tools` or `poetry` for dependency management and lock files

### 7. UI/UX Enhancements
- [ ] Use a resource file or stylesheet for consistent UI theming
- [ ] Implement dynamic dropdowns/radio buttons for product-specific options
- [ ] Review UI for accessibility best practices

### 8. Export & Integration
- [ ] Encapsulate all export logic in `src/export/`
- [ ] Decouple export logic from UI to allow CLI or API-triggered exports

### 9. Performance Optimization
- [ ] Profile and optimize slow code paths
- [ ] Ensure frequently queried fields are indexed in the database

### 10. Advanced Enhancements (Optional/Future)
- [ ] Consider using `pydantic` or `dynaconf` for configuration management
- [ ] Add authentication/authorization if multi-user
- [ ] Build admin UI for managing products, materials, and pricing rules

---

## How to Use This Plan
- Check off items as they are completed.
- Add notes, links to relevant files, or references to issues as needed.
- Update priorities as the project evolves.

## Related Files
- `README.md`: Project overview and setup
- `project_notes.md`: Design notes, ideas, and open questions
- `DECISIONS.md`: Architectural decisions and rationale (if present)

---

Welcome! Start here, and refer to the README for more details. 