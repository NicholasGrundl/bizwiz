# Issue: Code Quality Fixes

**Priority**: Medium
**Category**: Code Quality
**Estimated Effort**: Small (0.5-1 day)
**Can be parallelized**: Yes (independent fixes)

## Description

Several code quality issues exist that should be addressed:
- Duplicate imports
- TODO comments in production code
- Typos in configuration files
- Inconsistent type hints
- Missing error handling

## Current State

### Identified Issues:

1. **src/bizwiz/data.py:1 and :5** - Duplicate `import pathlib`
2. **src/bizwiz/llm.py:82** - TODO comment for error handling
3. **src/bizwiz/trade_data.py:163-164** - TODO comments about duplicates and fuzzy search
4. **setup.cfg:8** - Typo: "forCommon" should be "for Common"
5. **setup.cfg:13** - Incorrect key: "packages_dir" should be "packages.dir"
6. **Inconsistent type hints** - Some functions lack type hints
7. **Limited error handling** - Many functions don't handle edge cases

## Proposed Solution

### 1. Fix Duplicate Import

**File**: `src/bizwiz/data.py`

Remove the duplicate import on line 5:
```python
"""Manage paths to data and files"""

import pathlib
from typing import Union

# Remove duplicate: import pathlib  <-- DELETE THIS

PathType = Union[str, pathlib.Path]
```

### 2. Implement Error Handling in llm.py

**File**: `src/bizwiz/llm.py:82`

Replace TODO with actual error handling:
```python
def prompt(
    self,
    text : str,
    image_filepath : str | pathlib.Path | None = None,
)-> str:
    """Prompt the model with a message and return the answer"""
    try:
        messages = [message for message in self.conversation]
        message = self.get_message(text=text, image_filepath=image_filepath)

        messages.append(message)

        client = self.client
        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=self.system_prompt,
            messages=messages,
            temperature=self.temperature,
        )

        answer = response.content[-1].text

        # Update conversation
        self.conversation.append(message)
        self.conversation.append({'role' : 'assistant', 'content' : answer})
        return answer

    except anthropic.APIError as e:
        raise RuntimeError(f"Anthropic API error: {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error during LLM prompt: {e}")
```

### 3. Address TODOs in trade_data.py

**File**: `src/bizwiz/trade_data.py:163-164`

Investigate the duplicates issue and either:
- Fix the underlying issue
- Document why duplicates exist
- Add deduplication logic if needed

### 4. Fix Typos in setup.cfg

**File**: `setup.cfg`

Line 8:
```diff
-description = Python package forCommon business tasks and utilities
+description = Python package for common business tasks and utilities
```

Line 13:
```diff
-packages_dir =
+[options.packages.find]
+where = src
```

And remove the redundant section at line 72-73.

### 5. Add Missing Type Hints

Review all functions and add type hints where missing:
```python
# Before
def load_country_data(file_path):
    countries = []
    # ...

# After
def load_country_data(file_path: str) -> List[Tuple[str, str, str]]:
    countries: List[Tuple[str, str, str]] = []
    # ...
```

### 6. Add Missing Dependencies to setup.cfg

**File**: `setup.cfg`

Add missing dependencies:
```python
install_requires =
    # ... existing deps ...
    comtradeapicall
    fuzzywuzzy
    python-Levenshtein
```

### 7. Improve Error Messages

Add more descriptive error messages throughout:
```python
# Before
raise FileNotFoundError(f"File not found: {filepath}")

# After
raise FileNotFoundError(
    f"Data file not found: {filepath}\n"
    f"Current data_dir: {self.data_dir}\n"
    f"Make sure the file exists in the data directory."
)
```

## Acceptance Criteria

- [ ] No duplicate imports
- [ ] All TODO comments resolved or converted to GitHub issues
- [ ] All typos fixed
- [ ] Error handling added to critical functions
- [ ] Type hints added to all public functions
- [ ] setup.cfg correctly formatted
- [ ] Missing dependencies added to setup.cfg
- [ ] Code passes ruff checks
- [ ] Code passes mypy checks

## Dependencies

- None (can start immediately)

## Related Issues

- #05-linting-configuration (will catch these issues)
- #06-type-checking-configuration (will catch missing type hints)
- #01-testing-infrastructure (tests will verify fixes)

## Implementation Steps

1. Fix duplicate import in data.py
2. Fix typos in setup.cfg
3. Add error handling to llm.py
4. Investigate and resolve TODOs in trade_data.py
5. Add type hints to all functions
6. Add missing dependencies to setup.cfg
7. Run ruff and mypy to verify fixes
8. Create tests for error handling

## Files to Modify

- `src/bizwiz/data.py`
- `src/bizwiz/llm.py`
- `src/bizwiz/trade_data.py`
- `setup.cfg`
- All module files for type hints

## Notes

- These are quick wins that improve code quality
- Should be done before adding more features
- Will make future development easier
- Fixes will be validated by linting/type checking once configured
