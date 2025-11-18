# Issue: Improve Docstrings

**Priority**: Low
**Category**: Documentation
**Estimated Effort**: Medium (1 day)
**Can be parallelized**: Yes (can work module by module)

## Description

While some functions have docstrings, they are inconsistent in style and completeness. Many functions lack:
- Parameter descriptions
- Return value descriptions
- Example usage
- Raised exceptions documentation

Consistent, comprehensive docstrings improve:
- Code maintainability
- API documentation generation
- Developer experience
- IDE auto-completion

## Current State

- ⚠️ Some functions have docstrings, others don't
- ⚠️ Mixed docstring styles (Google vs. Numpy vs. plain text)
- ❌ No examples in docstrings
- ❌ No raised exceptions documented
- ❌ Some docstrings are too brief

## Proposed Solution

### 1. Choose Docstring Convention

**Recommendation**: Google Style (already suggested in ruff config)

Example format:
```python
def function_name(param1: str, param2: int) -> bool:
    """Brief one-line description.

    Longer description that provides more context about what the
    function does and when you might use it.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When param1 is empty
        FileNotFoundError: When file doesn't exist

    Example:
        >>> result = function_name("hello", 42)
        >>> print(result)
        True
    """
    pass
```

### 2. Update Existing Docstrings

#### src/bizwiz/data.py

```python
class PathManager:
    """Manage file paths relative to a data directory.

    This class provides utilities for finding and validating files
    within a specified data directory.

    Args:
        data_dir: Path to the data directory

    Example:
        >>> pm = PathManager('/path/to/data')
        >>> csv_files = pm.find_data_files('csv')
        >>> important_file = pm.get_data_file('important.csv')
    """

    def get_data_file(self, filename: PathType) -> pathlib.Path:
        """Get the validated path to a file in the data directory.

        Args:
            filename: Name or relative path of the file within data_dir

        Returns:
            Absolute Path object to the file

        Raises:
            FileNotFoundError: If the file doesn't exist

        Example:
            >>> pm = PathManager('/data')
            >>> path = pm.get_data_file('countries.csv')
            >>> print(path)
            PosixPath('/data/countries.csv')
        """
```

#### src/bizwiz/llm.py

```python
class ChatManager:
    """Manage conversational interactions with Anthropic's Claude API.

    This class handles chat sessions including conversation history,
    system prompts, and multimodal inputs (text + images).

    Args:
        temperature: Sampling temperature (0.0-1.0). Lower is more deterministic.

    Attributes:
        client: Anthropic API client
        model: Model identifier (default: claude-3-5-sonnet-20240620)
        conversation: List of message dictionaries (chat history)
        system_prompt: System-level instructions for the model

    Raises:
        KeyError: If required API keys are not set in environment

    Example:
        >>> chat = ChatManager(temperature=0.0)
        >>> chat.set_system_prompt("You are a helpful analyst")
        >>> answer = chat.prompt("What is 2+2?")
        >>> print(answer)
        4
    """

    def prompt(
        self,
        text: str,
        image_filepath: str | pathlib.Path | None = None,
    ) -> str:
        """Send a message to the model and get a response.

        This method automatically maintains conversation history,
        allowing for multi-turn conversations. Optionally include
        an image with the message.

        Args:
            text: The user's message text
            image_filepath: Optional path to an image file (PNG or JPEG)

        Returns:
            The model's text response

        Raises:
            RuntimeError: If API call fails
            FileNotFoundError: If image_filepath doesn't exist

        Example:
            >>> chat = ChatManager()
            >>> response = chat.prompt("Describe this image",
            ...                        image_filepath="chart.png")
        """
```

#### src/bizwiz/trade_data.py

```python
def search_country_iso(
    keyword: str,
    countries: List[Tuple[str, str, str]]
) -> pd.DataFrame:
    """Search for countries using fuzzy matching and return ISO codes.

    Uses the Levenshtein distance algorithm to find countries
    matching the search keyword, even with typos.

    Args:
        keyword: Country name or partial name to search for
        countries: List of (name, alpha-2, alpha-3) tuples

    Returns:
        DataFrame with columns: name, iso, score
        Sorted by match score (descending)

    Example:
        >>> countries = load_country_data('countries.csv')
        >>> results = search_country_iso('united states', countries)
        >>> print(results)
           name                    iso  score
        0  United States of America  USA    95
        1  United States Minor...    UMI    75
    """
```

### 3. Add Module-Level Docstrings

Each module should have a docstring:

```python
"""Trade data retrieval and analysis.

This module provides functions for:
- Searching countries and commodities using fuzzy matching
- Fetching historical trade data from UN Comtrade API
- Processing and analyzing trade flows
- Calculating trade metrics and visualizations

The main workflow is:
1. Search for country/commodity codes
2. Fetch raw trade data
3. Process and clean the data
4. Calculate metrics and create visualizations

Example:
    >>> from bizwiz.trade_data import search_country_iso, get_trade_data
    >>> countries = load_country_data('data/iso_codes.csv')
    >>> usa = search_country_iso('USA', countries)
    >>> data = get_trade_data([842], '280700', [202201], api_key)
"""
```

### 4. Enable Docstring Linting

In ruff config, ensure docstring checks are enabled:
```toml
[tool.ruff]
select = [
    # ... other rules ...
    "D",  # pydocstyle - docstring conventions
]

[tool.ruff.lint.pydocstyle]
convention = "google"
```

## Acceptance Criteria

- [ ] All public functions have complete docstrings
- [ ] All classes have docstrings with examples
- [ ] All modules have module-level docstrings
- [ ] Docstrings follow Google style consistently
- [ ] Examples included in key function docstrings
- [ ] Raised exceptions documented
- [ ] Docstrings pass pydocstyle/ruff checks

## Dependencies

- **Recommended**: #05-linting-configuration (for docstring linting)

## Related Issues

- #03-documentation-improvements (docstrings feed into API docs)
- #06-type-checking-configuration (type hints and docstrings should match)

## Implementation Steps

1. Add module-level docstrings to all modules
2. Update class docstrings in data.py
3. Update class docstrings in llm.py
4. Add function docstrings to trade_data.py (many missing)
5. Add function docstrings to image.py
6. Add examples to critical functions
7. Enable pydocstyle in ruff config
8. Run ruff to verify docstring compliance
9. Fix any issues found

## Priority Order

1. **High Priority**:
   - `ChatManager` class (public API)
   - `PathManager` class (public API)
   - `load_country_data`, `search_country_iso`, `get_trade_data` (core functions)

2. **Medium Priority**:
   - Image processing functions
   - Helper functions in trade_data.py

3. **Low Priority**:
   - Internal utility functions
   - Private methods

## Notes

- Google style is clean and readable
- Examples in docstrings serve as mini-tests
- Good docstrings make API documentation generation trivial
- Consider using `sphinx.ext.napoleon` or `mkdocstrings` to generate docs from docstrings
