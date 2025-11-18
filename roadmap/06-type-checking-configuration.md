# Issue: Type Checking Configuration

**Priority**: Medium
**Category**: Code Quality / Tooling
**Estimated Effort**: Small (2-3 hours)
**Can be parallelized**: Yes (with linting configuration)

## Description

The project has `mypy` installed in requirements-dev.txt but no configuration. Type hints are used inconsistently throughout the codebase. Proper type checking would:
- Catch type-related bugs early
- Improve code documentation
- Enable better IDE support
- Make refactoring safer

## Current State

- ✅ mypy installed in requirements-dev.txt
- ❌ No mypy configuration
- ⚠️ Inconsistent type hints usage
- ⚠️ Using `str | pathlib.Path` syntax (requires Python 3.10+)
- ⚠️ Some functions use old-style Union type hints
- ❌ No type checking in development workflow

## Proposed Solution

### 1. Create mypy Configuration

Add to `pyproject.toml`:

```toml
[tool.mypy]
# Python version
python_version = "3.10"

# Source directories
files = ["src/bizwiz"]

# Strictness levels
strict = false  # Start with false, gradually enable
warn_return_any = true
warn_unused_configs = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true

# Error messages
show_error_context = true
show_column_numbers = true
show_error_codes = true
pretty = true

# Import discovery
namespace_packages = true
explicit_package_bases = true

# Untyped definitions
check_untyped_defs = true
disallow_untyped_defs = false  # Start with false, enable module by module
disallow_incomplete_defs = true
disallow_untyped_calls = false  # Start with false

# Miscellaneous
warn_unused_ignores = true
follow_imports = "normal"

# Per-module options
[[tool.mypy.overrides]]
module = "bizwiz.llm"
disallow_untyped_defs = true  # Enforce strict typing in critical modules

[[tool.mypy.overrides]]
module = "bizwiz.data"
disallow_untyped_defs = true

# Third-party libraries without type stubs
[[tool.mypy.overrides]]
module = [
    "comtradeapicall.*",
    "fuzzywuzzy.*",
    "anthropic.*",
    "PIL.*",
    "pandas.*",
    "matplotlib.*",
    "seaborn.*",
    "plotly.*",
    "streamlit.*",
    "panel.*",
    "burr.*",
    "hamilton.*",
]
ignore_missing_imports = true
```

### 2. Add Type Hints to All Functions

**Priority files** to add type hints:

#### src/bizwiz/data.py
```python
from typing import Union, List
import pathlib

PathType = Union[str, pathlib.Path]

class PathManager:
    def __init__(self, data_dir: PathType) -> None:
        self.data_dir = data_dir

    @property
    def data_dir(self) -> pathlib.Path:
        return self._data_dir

    @data_dir.setter
    def data_dir(self, path: PathType) -> None:
        self._data_dir = pathlib.Path(path)

    def get_data_file(self, filename: PathType) -> pathlib.Path:
        # ... implementation

    def find_data_files(self, suffix: str | None = None) -> List[str]:
        # ... implementation
```

#### src/bizwiz/llm.py
Already has good type hints, but needs:
```python
from typing import Any, Dict, List
from pathlib import Path

def load_llm_env(llm_vendors: List[str] | None = None) -> bool:
    # ... implementation

def get_message(
    self,
    text: str,
    image_filepath: str | Path | None = None
) -> Dict[str, Any]:
    # ... implementation
```

#### src/bizwiz/trade_data.py
Many functions missing type hints:
```python
from typing import List, Tuple
import pandas as pd

def load_country_data(file_path: str) -> List[Tuple[str, str, str]]:
    # ... implementation

def fuzzy_search_country(
    query: str,
    countries: List[Tuple[str, str, str]],
    limit: int = 5
) -> List[Tuple[str, str, str, int]]:
    # ... implementation

def filter_df_date(
    df: pd.DataFrame,
    start_date: str,
    end_date: str,
    date_column: str = 'date'
) -> pd.DataFrame:
    # ... implementation
```

### 3. Create Type Stubs for Third-Party Libraries

If type stubs are needed for critical libraries:
```bash
# Install type stubs
pip install types-requests types-Pillow
```

Add to requirements-dev.txt:
```
types-requests
types-Pillow
```

### 4. Add Makefile Targets

Add to `Makefile`:
```makefile
.PHONY: typecheck
typecheck:
	@echo "Running mypy type checker..."
	mypy src/

.PHONY: typecheck.report
typecheck.report:
	@echo "Generating mypy report..."
	mypy src/ --html-report ./mypy-report
	@echo "Report generated in ./mypy-report/"
```

### 5. Gradually Enable Strict Mode

Once initial type hints are added:
1. Enable `disallow_untyped_defs = true` module by module
2. Eventually enable `strict = true` for the entire project
3. Add type hints to all functions progressively

### 6. Document in README

Add to README.md:
```markdown
## Type Checking

Run type checking:
\```bash
make typecheck
\```

Generate HTML report:
\```bash
make typecheck.report
\```

The project uses mypy for static type checking. All public functions should have type hints.
```

## Acceptance Criteria

- [ ] mypy configuration added to pyproject.toml
- [ ] Type hints added to all public functions
- [ ] mypy runs without errors on strict modules
- [ ] Type stubs installed for critical dependencies
- [ ] Makefile targets created
- [ ] README updated with type checking instructions
- [ ] CI/CD configured to run mypy (see #02)

## Dependencies

- None (can start immediately)

## Related Issues

- #02-ci-cd-pipeline (will include type checking in CI)
- #04-code-quality-fixes (fixes should be type-safe)
- #05-linting-configuration (complementary tooling)
- #07-improve-docstrings (docstrings should match type hints)

## Implementation Steps

1. Add mypy configuration to pyproject.toml
2. Install missing type stubs
3. Run mypy to see current state: `mypy src/`
4. Add type hints to data.py (easiest first)
5. Add type hints to image.py
6. Add type hints to trade_data.py
7. Add type hints to llm.py
8. Fix any type errors found by mypy
9. Add Makefile targets
10. Update README
11. Gradually enable stricter settings

## Current Type Hint Status

### Good:
- `src/bizwiz/llm.py` - Most functions have type hints
- `src/bizwiz/data.py` - Basic type hints present

### Needs Improvement:
- `src/bizwiz/trade_data.py` - Many functions lack return type hints
- `src/bizwiz/image.py` - Some functions lack type hints
- Inconsistent use of Union vs | syntax

## Notes

- Python 3.10+ supports `str | None` syntax instead of `Union[str, None]`
- Stick to one style throughout the project
- pandas type hints can be tricky - may need `# type: ignore` in some places
- Consider using `pandas-stubs` for better pandas type checking
- Type checking catches bugs early and improves code quality significantly
