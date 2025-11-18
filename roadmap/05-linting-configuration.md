# Issue: Linting Configuration

**Priority**: Medium
**Category**: Code Quality / Tooling
**Estimated Effort**: Small (2-3 hours)
**Can be parallelized**: Yes (with type checking configuration)

## Description

The project has `ruff` installed in requirements-dev.txt but no configuration file. This means:
- No consistent code style enforcement
- No automatic code quality checks
- No format checking
- Inconsistent import sorting

## Current State

- ✅ ruff installed in requirements-dev.txt
- ❌ No `ruff.toml` or `pyproject.toml` ruff configuration
- ❌ No consistent style enforcement
- ✅ Some style config exists in setup.cfg for flake8 (deprecated)
- ❌ No automatic fixing on save

## Proposed Solution

### 1. Create ruff Configuration

Add to `pyproject.toml`:

```toml
[tool.ruff]
# Minimum Python version
target-version = "py310"

# Line length
line-length = 100

# Source directory
src = ["src"]

# Enable specific rule sets
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # pyflakes
    "I",      # isort
    "N",      # pep8-naming
    "UP",     # pyupgrade
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "DTZ",    # flake8-datetimez
    "T10",    # flake8-debugger
    "ISC",    # flake8-implicit-str-concat
    "ICN",    # flake8-import-conventions
    "PIE",    # flake8-pie
    "PT",     # flake8-pytest-style
    "Q",      # flake8-quotes
    "RSE",    # flake8-raise
    "RET",    # flake8-return
    "SIM",    # flake8-simplify
    "PTH",    # flake8-use-pathlib
    "PD",     # pandas-vet
    "PL",     # pylint
    "RUF",    # ruff-specific rules
]

# Ignore specific rules
ignore = [
    "E501",   # line too long (handled by formatter)
    "PLR0913", # too many arguments
    "PLR2004", # magic value comparison
]

# Exclude directories
exclude = [
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "build",
    "dist",
    "*.egg-info",
    "notebooks",  # Exclude notebooks from linting
]

[tool.ruff.format]
# Use double quotes
quote-style = "double"

# Indent with 4 spaces
indent-style = "space"

# Unix line endings
line-ending = "auto"

[tool.ruff.lint.isort]
# Import sorting configuration
known-first-party = ["bizwiz"]
section-order = ["future", "standard-library", "third-party", "first-party", "local-folder"]

[tool.ruff.lint.per-file-ignores]
# Allow unused imports in __init__.py
"__init__.py" = ["F401"]
# Allow print statements in example scripts
"examples/*.py" = ["T201"]

[tool.ruff.lint.pydocstyle]
# Use Google-style docstrings
convention = "google"
```

### 2. Remove Deprecated flake8 and isort Config

Remove or comment out in `setup.cfg`:
```ini
# [flake8]  # DEPRECATED - now using ruff
# [isort]   # DEPRECATED - now using ruff
```

### 3. Add Makefile Targets for Linting

Add to `Makefile`:
```makefile
#### Code Quality ####
.PHONY: lint
lint:
	@echo "Running ruff linter..."
	ruff check src/

.PHONY: lint.fix
lint.fix:
	@echo "Running ruff with auto-fix..."
	ruff check --fix src/

.PHONY: format
format:
	@echo "Formatting code with ruff..."
	ruff format src/

.PHONY: format.check
format.check:
	@echo "Checking code formatting..."
	ruff format --check src/
```

### 4. Run Initial Linting

Run ruff to identify existing issues:
```bash
ruff check src/
```

Fix auto-fixable issues:
```bash
ruff check --fix src/
```

Format code:
```bash
ruff format src/
```

### 5. Document in README

Add to README.md:
```markdown
## Code Quality

### Linting

Check code quality:
\```bash
make lint
\```

Auto-fix issues:
\```bash
make lint.fix
\```

### Formatting

Check formatting:
\```bash
make format.check
\```

Format code:
\```bash
make format
\```
```

## Acceptance Criteria

- [ ] ruff configuration added to pyproject.toml
- [ ] All ruff checks pass on src/
- [ ] Code formatted with ruff
- [ ] Makefile targets created for linting
- [ ] Deprecated flake8/isort config removed
- [ ] README updated with linting instructions
- [ ] Pre-commit hook configured (see #02)

## Dependencies

- None (can start immediately)

## Related Issues

- #02-ci-cd-pipeline (will include linting in CI)
- #04-code-quality-fixes (fixes should pass linting)
- #06-type-checking-configuration (complementary tooling)

## Implementation Steps

1. Add ruff configuration to pyproject.toml
2. Remove deprecated flake8/isort config from setup.cfg
3. Run `ruff check src/` to see current issues
4. Fix auto-fixable issues with `ruff check --fix src/`
5. Manually fix remaining issues
6. Run `ruff format src/` to format code
7. Add Makefile targets
8. Update README
9. Commit changes

## Expected Findings

When first running ruff, expect to find:
- Import sorting issues
- Unused imports
- Line length violations
- Missing docstrings
- Complexity issues
- Potential bugs (undefined names, etc.)

## Notes

- Ruff is much faster than flake8 + isort + pyupgrade combined
- It's compatible with most flake8 plugins
- Can auto-fix many issues
- The configuration above is opinionated but follows Python best practices
- Adjust rules as needed for project preferences
