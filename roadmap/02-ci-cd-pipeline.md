# Issue: CI/CD Pipeline

**Priority**: High
**Category**: DevOps
**Estimated Effort**: Small (0.5-1 day)
**Can be parallelized**: Partially (needs tests to exist first)

## Description

The project has no automated continuous integration or deployment pipeline. This means:
- No automated testing on pull requests
- No automated linting/formatting checks
- No automated version bumping or releases
- Manual quality control only

## Current State

- ❌ No `.github/workflows/` directory
- ❌ No GitHub Actions configured
- ❌ No automated testing
- ❌ No automated releases
- ✅ Make targets exist for some operations

## Proposed Solution

### 1. Create GitHub Actions Workflows

#### CI Workflow (`.github/workflows/ci.yml`)
```yaml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    - name: Run tests
      run: pytest --cov --cov-report=xml
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

#### Linting Workflow (`.github/workflows/lint.yml`)
```yaml
name: Lint

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: "3.10"
    - name: Install dependencies
      run: pip install ruff mypy
    - name: Run ruff
      run: ruff check src/
    - name: Run mypy
      run: mypy src/
```

#### Release Workflow (`.github/workflows/release.yml`)
- Triggered on tag creation
- Builds package
- Publishes to PyPI (if desired)

### 2. Add Pre-commit Hooks

Create `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
```

### 3. Add Status Badges to README

```markdown
[![CI](https://github.com/NicholasGrundl/bizwiz/workflows/CI/badge.svg)](https://github.com/NicholasGrundl/bizwiz/actions)
[![codecov](https://codecov.io/gh/NicholasGrundl/bizwiz/branch/main/graph/badge.svg)](https://codecov.io/gh/NicholasGrundl/bizwiz)
```

## Acceptance Criteria

- [ ] GitHub Actions CI workflow created and passing
- [ ] GitHub Actions lint workflow created and passing
- [ ] Tests run on Python 3.10, 3.11, and 3.12
- [ ] Coverage reports uploaded to Codecov (or similar)
- [ ] Pre-commit hooks configured
- [ ] Status badges added to README
- [ ] All workflows documented

## Dependencies

- **Requires**: #01-testing-infrastructure (tests must exist)
- **Requires**: #05-linting-configuration (ruff config)
- **Requires**: #06-type-checking-configuration (mypy config)

## Related Issues

- #01-testing-infrastructure
- #05-linting-configuration
- #06-type-checking-configuration

## Implementation Steps

1. Create `.github/workflows/` directory
2. Create `ci.yml` workflow
3. Create `lint.yml` workflow
4. Test workflows on a feature branch
5. Create `.pre-commit-config.yaml`
6. Add pre-commit to requirements-dev.txt
7. Update README with setup instructions and badges
8. (Optional) Set up Codecov account and add token to GitHub secrets

## Notes

- Start with basic CI/CD, can enhance later
- Consider adding dependabot for dependency updates
- May want to add workflow for notebook execution/validation
- Could add automatic roadmap checking/project board updates
