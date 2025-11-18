# Issue: Package Structure Improvements

**Priority**: Low
**Category**: Architecture
**Estimated Effort**: Medium (1 day)
**Can be parallelized**: No (requires code refactoring)

## Description

The current package structure could be improved for better organization and maintainability:
- All modules are at the top level of `src/bizwiz/`
- No subpackages for logical grouping
- Some module names could be more descriptive
- No clear separation of concerns

## Current State

```
src/bizwiz/
├── __init__.py
├── data.py         # Path management
├── llm.py          # LLM chat management
├── image.py        # Image processing
└── trade_data.py   # Trade data fetching and analysis
```

### Issues:
- ❌ Flat structure makes it hard to navigate as package grows
- ❌ `data.py` is too generic (just has PathManager)
- ❌ `trade_data.py` has multiple responsibilities
- ❌ No separation between API clients and data processing

## Proposed Solution

### Option 1: Organize by Domain

```
src/bizwiz/
├── __init__.py
├── config.py              # Configuration management
│
├── core/                  # Core utilities
│   ├── __init__.py
│   └── paths.py          # PathManager (from data.py)
│
├── llm/                   # LLM integrations
│   ├── __init__.py
│   ├── chat.py           # ChatManager (from llm.py)
│   ├── image.py          # Image processing (from image.py)
│   └── extractors.py     # Data extraction utilities
│
├── trade/                 # Trade data analysis
│   ├── __init__.py
│   ├── client.py         # Comtrade API client
│   ├── search.py         # Country/commodity fuzzy search
│   ├── processing.py     # Data processing functions
│   ├── metrics.py        # Trade metrics calculations
│   └── visualization.py  # Plotting functions
│
└── data/                  # Data source integrations
    ├── __init__.py
    ├── comtrade.py       # UN Comtrade API
    ├── eia.py            # EIA API
    └── undata.py         # UN Data API
```

### Option 2: Organize by Function

```
src/bizwiz/
├── __init__.py
├── config.py
│
├── api/                   # External API clients
│   ├── __init__.py
│   ├── comtrade.py
│   ├── eia.py
│   ├── openai.py
│   └── anthropic.py
│
├── processing/            # Data processing
│   ├── __init__.py
│   ├── trade.py
│   ├── solubility.py
│   └── tables.py
│
├── extraction/            # Data extraction
│   ├── __init__.py
│   ├── pdf.py
│   ├── images.py
│   └── screenshots.py
│
├── analysis/              # Analysis tools
│   ├── __init__.py
│   ├── metrics.py
│   └── visualization.py
│
└── utils/                 # Utilities
    ├── __init__.py
    ├── paths.py
    ├── fuzzy_search.py
    └── dates.py
```

### Recommendation: Option 1 (Organize by Domain)

This makes the most sense for the current use case.

## Migration Plan

### Phase 1: Create New Structure

1. Create new directory structure
2. Move code to new locations
3. Update imports in moved modules
4. Update `__init__.py` to maintain backward compatibility

### Phase 2: Refactor trade_data.py

Split `trade_data.py` into logical modules:

**`trade/client.py`** - API client:
```python
"""Comtrade API client."""

class ComtradeClient:
    """Client for UN Comtrade API."""

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_available_data(self, country: int) -> pd.DataFrame:
        """Get available data for a country."""
        pass

    def get_trade_data(
        self,
        country: int,
        commodity: str,
        periods: list[int],
        flow: str = 'import'
    ) -> pd.DataFrame:
        """Fetch trade data."""
        pass
```

**`trade/search.py`** - Search functionality:
```python
"""Country and commodity search."""

def load_country_data(file_path: str) -> list[tuple[str, str, str]]:
    """Load country codes from CSV."""
    pass

def search_country(keyword: str, countries: list) -> pd.DataFrame:
    """Fuzzy search for countries."""
    pass

def search_commodity(keyword: str, hs_version: str = 'HS') -> pd.DataFrame:
    """Fuzzy search for commodity codes."""
    pass
```

**`trade/processing.py`** - Data processing:
```python
"""Trade data processing."""

def process_trade_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and process raw trade data."""
    pass

def filter_by_date(
    df: pd.DataFrame,
    start: str,
    end: str
) -> pd.DataFrame:
    """Filter dataframe by date range."""
    pass
```

**`trade/metrics.py`** - Metrics calculation:
```python
"""Trade metrics calculation."""

def calculate_trade_metrics(
    import_df: pd.DataFrame,
    export_df: pd.DataFrame
) -> dict:
    """Calculate trade metrics."""
    pass
```

**`trade/visualization.py`** - Plotting:
```python
"""Trade data visualization."""

def plot_annotated_scatter(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    color_col: str
) -> Figure:
    """Create annotated scatter plot."""
    pass
```

### Phase 3: Update Main __init__.py

Maintain backward compatibility:
```python
"""Python package for common business tasks and utilities."""

# Version info
__version__ = (0, 1, 0)
__author__ = "Nick Grundl"

# Legacy imports (for backward compatibility)
from .core.paths import PathManager
from .llm.chat import ChatManager, load_llm_env

# New imports (recommended)
from .config import get_config, load_config
from . import trade
from . import llm
from . import core

__all__ = [
    # Legacy
    'PathManager',
    'ChatManager',
    'load_llm_env',
    # New
    'get_config',
    'load_config',
    'trade',
    'llm',
    'core',
]
```

### Phase 4: Update Documentation

Update all documentation to reflect new structure:
```python
# Old way (still works)
from bizwiz import ChatManager

# New way (recommended)
from bizwiz.llm import ChatManager

# Or
import bizwiz.llm as llm
chat = llm.ChatManager()
```

## Acceptance Criteria

- [ ] New package structure implemented
- [ ] All code moved to appropriate modules
- [ ] Backward compatibility maintained
- [ ] All imports updated
- [ ] Tests updated for new structure
- [ ] Documentation updated
- [ ] README shows both old and new import styles
- [ ] CHANGELOG documents the restructure

## Dependencies

- **Recommended**: #01-testing-infrastructure (need tests to ensure nothing breaks)
- **Recommended**: #04-code-quality-fixes (clean code before moving)

## Related Issues

- #01-testing-infrastructure
- #03-documentation-improvements

## Implementation Steps

1. Create new directory structure
2. Create new module files with proper docstrings
3. Move code from old modules to new modules
4. Refactor as needed
5. Update imports in all modules
6. Update `__init__.py` for backward compatibility
7. Run tests to ensure nothing broke
8. Update all imports in notebooks
9. Update documentation
10. Update examples
11. Add deprecation warnings to old import paths (optional)

## Breaking Changes

This can be done WITHOUT breaking changes by:
1. Maintaining imports in top-level `__init__.py`
2. Adding deprecation warnings for old imports
3. Supporting both old and new import styles for one major version

Example:
```python
# bizwiz/__init__.py
import warnings

def _deprecated_import():
    warnings.warn(
        "Importing from bizwiz root is deprecated. "
        "Use 'from bizwiz.llm import ChatManager' instead.",
        DeprecationWarning,
        stacklevel=2
    )

# Old imports still work but show deprecation warning
class ChatManager(_ChatManager):
    def __init__(self, *args, **kwargs):
        _deprecated_import()
        super().__init__(*args, **kwargs)
```

## Notes

- Better organization scales as project grows
- Clear module boundaries improve maintainability
- Subpackages make it clear where functionality lives
- Can be done incrementally
- Tests are crucial to ensure refactoring doesn't break things
