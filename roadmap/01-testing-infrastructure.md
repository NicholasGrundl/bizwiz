# Issue: Testing Infrastructure

**Priority**: High
**Category**: Testing
**Estimated Effort**: Medium (1-2 days)
**Can be parallelized**: Yes (with other documentation/config tasks)

## Description

The project currently has **zero test coverage** despite having pytest and pytest-cov installed in `requirements-dev.txt`. This is a critical gap that needs to be addressed to ensure code quality and prevent regressions.

## Current State

- ✅ pytest installed in requirements-dev.txt
- ✅ pytest configuration exists in pyproject.toml
- ❌ No tests/ directory
- ❌ No test files
- ❌ No test coverage reports
- ❌ No CI/CD running tests

## Proposed Solution

### 1. Create Test Directory Structure
```
tests/
├── __init__.py
├── conftest.py
├── test_data.py
├── test_llm.py
├── test_image.py
├── test_trade_data.py
└── fixtures/
    ├── sample_images/
    └── sample_data/
```

### 2. Write Unit Tests

**Priority modules to test:**
- `src/bizwiz/data.py` - PathManager class
- `src/bizwiz/image.py` - Image loading and encoding
- `src/bizwiz/trade_data.py` - Data processing functions
- `src/bizwiz/llm.py` - ChatManager (with mocked API calls)

### 3. Add Test Coverage Configuration

Add to `pyproject.toml`:
```toml
[tool.coverage.run]
source = ["src/bizwiz"]
omit = ["*/tests/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
]
```

### 4. Create Test Fixtures

- Sample CSV files for trade data testing
- Sample images (PNG, JPEG) for image processing tests
- Mock API responses for LLM and Comtrade API calls

## Acceptance Criteria

- [ ] tests/ directory created with proper structure
- [ ] At least 50% code coverage for each module
- [ ] All tests pass with `pytest`
- [ ] Coverage report generated with `pytest --cov`
- [ ] Fixtures created for reusable test data
- [ ] Mock API calls properly implemented (no actual API calls in tests)

## Dependencies

- None (can start immediately)

## Related Issues

- #02-ci-cd-pipeline (tests should run in CI/CD)
- #04-code-quality-fixes (fixes can have tests written alongside)

## Implementation Steps

1. Create tests/ directory structure
2. Write conftest.py with common fixtures
3. Write tests for data.py (easiest, no external dependencies)
4. Write tests for image.py
5. Write tests for trade_data.py with mocked API calls
6. Write tests for llm.py with mocked Anthropic API
7. Run coverage report and aim for >70% coverage
8. Document how to run tests in README

## Notes

- Use `pytest-mock` for mocking external API calls
- Consider adding `pytest-vcr` for recording/replaying HTTP interactions
- Environment variables (API keys) should not be required for tests to run
