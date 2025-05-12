# MyBabbittQuote

A modern, domain-driven quote generator for Babbitt International products. This application provides a user-friendly interface for configuring, pricing, and quoting complex industrial products, with robust business logic and export capabilities.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Directory Structure](#directory-structure)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Testing](#testing)
- [Contributing](#contributing)
- [Related Files](#related-files)
- [License](#license)

---

## Project Overview
- **Purpose:** Streamline the process of configuring, pricing, and quoting Babbitt International products.
- **Features:**
  - Tabbed UI for product selection, specifications, quote summary, and spare parts
  - Complex pricing logic with material, length, and option rules
  - Quote management and export (PDF planned)
  - Extensible, maintainable, and testable codebase

## Directory Structure
```
MyBabbittQuote/
  src/           # Main application source code
    core/        # Business logic, models, services
    ui/          # User interface (PySide6)
    export/      # Export logic (PDF, etc.)
    utils/       # Shared utilities
  scripts/       # Automation, data, and test scripts
  tests/         # Unit and integration tests
  data/          # Data files (price lists, etc.)
  migrations/    # Database migrations (Alembic)
  myenv/         # (Optional) Virtual environment
  ACTION_PLAN.md # Prioritized action plan
  project_notes.md # Design notes and ideas
  README.md      # This file
  requirements.txt # Python dependencies
  setup.py       # (Optional) Project setup script
  main.py        # Application entry point
```

## Setup & Installation
1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd MyBabbittQuote
   ```
2. **Create and activate a virtual environment (recommended):**
   ```sh
   python -m venv myenv
   .\myenv\Scripts\activate  # On Windows
   # Or: source myenv/bin/activate  # On Linux/Mac
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Initialize the database:**
   ```sh
   python scripts/create_db.py
   ```

## Usage
- **Start the application:**
  ```sh
  python main.py
  ```
- **Navigate the UI:**
  - Select products, configure specifications, and generate quotes.
  - Save or export quotes (PDF export in progress).

## Testing
- **Run all tests:**
  ```sh
  pytest
  ```
- **Run specific test scripts:**
  ```sh
  python scripts/test_pricing.py
  python scripts/test_business_logic.py
  # ...etc.
  ```
- **Test database and business logic:**
  - See `tests/` and `scripts/` for available test modules.

## Contributing
- **Start here:**
  - Read `ACTION_PLAN.md` for current priorities and next steps.
  - Review `project_notes.md` for design ideas and open questions.
- **Guidelines:**
  - Follow code style and organization conventions (see `ACTION_PLAN.md` and comments).
  - Write clear docstrings and comments for complex logic.
  - Add or update tests for new features and bug fixes.
  - Update documentation as needed.

## Related Files
- [`ACTION_PLAN.md`](./ACTION_PLAN.md): Prioritized action plan and onboarding
- [`project_notes.md`](./project_notes.md): Design notes, ideas, and open questions
- [`requirements.txt`](./requirements.txt): Python dependencies
- [`main.py`](./main.py): Application entry point

## License
_This project is for internal use. Add license information here if needed._

---

**Welcome! Start by reading `ACTION_PLAN.md` and this README.**
