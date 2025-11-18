# Issue: Dependency Management

**Priority**: Low
**Category**: Project Configuration
**Estimated Effort**: Small (0.5 day)
**Can be parallelized**: Yes (independent task)

## Description

The project has several dependency management issues:
- No version pinning in requirements.txt
- Inconsistencies between requirements.txt and setup.cfg
- Very heavy dependency list (40+ packages)
- No differentiation between core and optional dependencies
- No dependency vulnerability scanning

## Current State

### Issues Identified:

1. **No Version Pinning**
   - requirements.txt has no version constraints
   - Could lead to breaking changes when dependencies update
   - Hard to reproduce environments

2. **Missing Dependencies in setup.cfg**
   - `comtradeapicall` in requirements.txt but not setup.cfg
   - `fuzzywuzzy` in requirements.txt but not setup.cfg
   - `python-Levenshtein` in requirements.txt but not setup.cfg

3. **Heavy Dependencies**
   - 40+ packages required
   - Many may not be actively used
   - Large install size and time
   - Potential security vulnerabilities

4. **No Optional Dependencies**
   - All dependencies are required
   - Could have optional extras for specific use cases

## Proposed Solution

### 1. Pin Dependency Versions

Create `requirements-lock.txt` with pinned versions:
```bash
pip freeze > requirements-lock.txt
```

Or use `pip-tools`:
```bash
pip install pip-tools
pip-compile requirements.txt -o requirements-lock.txt
pip-compile requirements-dev.txt -o requirements-dev-lock.txt
```

### 2. Sync setup.cfg with requirements.txt

Update `setup.cfg`:
```ini
install_requires =
    # General
    requests>=2.31.0
    click>=8.1.0
    python-dotenv>=1.0.0
    isodate>=0.6.1
    nanoid>=2.0.0
    fuzzywuzzy>=0.18.0
    python-Levenshtein>=0.21.0

    # Spreadsheets
    openpyxl>=3.1.0
    xlsxwriter>=3.1.0
    gspread>=5.11.0

    # Scientific
    numpy>=1.24.0
    pandas>=2.0.0
    scipy>=1.11.0

    # Datamodel
    pydantic>=2.0.0

    # Graph/Networks
    networkx>=3.1.0
    graphviz>=0.20.0

    # Visualization
    matplotlib>=3.7.0
    seaborn>=0.12.0
    plotly>=5.17.0

    # PDF/RAG
    PyMuPDF>=1.23.0
    llama-index>=0.9.0
    spacy>=3.7.0

    # AI and ML
    scikit-learn>=1.3.0
    tiktoken>=0.5.0
    openai>=1.3.0
    anthropic>=0.7.0
    instructor>=0.4.0

    # Orchestration
    burr[start]>=0.1.0
    sf-hamilton[visualization]>=1.0.0

    # UI
    panel>=1.3.0
    ipywidgets>=8.1.0
    ipycytoscape>=1.3.0
    streamlit>=1.28.0

    # APIs
    comtradeapicall>=0.1.0
```

### 3. Create Optional Dependencies

Reorganize into core and optional dependencies:

```ini
[options]
install_requires =
    # Core dependencies only
    requests>=2.31.0
    click>=8.1.0
    python-dotenv>=1.0.0
    numpy>=1.24.0
    pandas>=2.0.0
    anthropic>=0.7.0
    comtradeapicall>=0.1.0
    fuzzywuzzy>=0.18.0
    python-Levenshtein>=0.21.0
    openpyxl>=3.1.0

[options.extras_require]
llm =
    openai>=1.3.0
    anthropic>=0.7.0
    tiktoken>=0.5.0
    instructor>=0.4.0

pdf =
    PyMuPDF>=1.23.0
    llama-index>=0.9.0
    spacy>=3.7.0

viz =
    matplotlib>=3.7.0
    seaborn>=0.12.0
    plotly>=5.17.0

ui =
    streamlit>=1.28.0
    panel>=1.3.0
    ipywidgets>=8.1.0
    ipycytoscape>=1.3.0

orchestration =
    burr[start]>=0.1.0
    sf-hamilton[visualization]>=1.0.0

all =
    bizwiz[llm,pdf,viz,ui,orchestration]
```

Then users can install with:
```bash
pip install bizwiz              # Core only
pip install bizwiz[llm]         # Core + LLM
pip install bizwiz[all]         # Everything
```

### 4. Audit Dependencies

Check which dependencies are actually used:
```bash
# Install pipreqs
pip install pipreqs

# Generate requirements from imports
pipreqs src/ --force
```

Compare with current requirements and remove unused ones.

### 5. Add Security Scanning

Add to `.github/workflows/security.yml`:
```yaml
name: Security

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.10"
      - name: Install dependencies
        run: |
          pip install safety pip-audit
      - name: Run safety check
        run: safety check --json
      - name: Run pip-audit
        run: pip-audit
```

### 6. Document Dependency Groups

Update README.md:
```markdown
## Installation

### Basic Installation
\```bash
pip install bizwiz
\```

### With LLM Support
\```bash
pip install bizwiz[llm]
\```

### With Visualization
\```bash
pip install bizwiz[viz]
\```

### Full Installation
\```bash
pip install bizwiz[all]
\```

### Development Installation
\```bash
pip install -e ".[all]"
pip install -r requirements-dev.txt
\```
```

## Acceptance Criteria

- [ ] All dependencies version-pinned
- [ ] setup.cfg and requirements.txt are in sync
- [ ] Optional dependency groups created
- [ ] Unused dependencies removed
- [ ] Security scanning configured
- [ ] README documents installation options
- [ ] Makefile has commands for dependency management

## Dependencies

- None (can start immediately)

## Related Issues

- #02-ci-cd-pipeline (will include security scanning)

## Implementation Steps

1. Audit current dependencies with pipreqs
2. Identify unused dependencies
3. Create core vs. optional dependency groups
4. Update setup.cfg with version pins
5. Create requirements-lock.txt
6. Add security scanning workflow
7. Update Makefile with dependency commands
8. Update README with installation options
9. Test installation in clean environment

## Makefile Targets to Add

```makefile
.PHONY: deps.lock
deps.lock:
	@echo "Generating locked requirements..."
	pip-compile requirements.txt -o requirements-lock.txt
	pip-compile requirements-dev.txt -o requirements-dev-lock.txt

.PHONY: deps.upgrade
deps.upgrade:
	@echo "Upgrading dependencies..."
	pip-compile --upgrade requirements.txt -o requirements-lock.txt

.PHONY: deps.audit
deps.audit:
	@echo "Auditing dependencies for security issues..."
	pip-audit
	safety check

.PHONY: deps.tree
deps.tree:
	@echo "Showing dependency tree..."
	pipdeptree
```

## Notes

- Consider using poetry or pdm for better dependency management
- Version pinning prevents "it works on my machine" issues
- Optional dependencies reduce install time for users who don't need everything
- Regular security audits prevent vulnerability exploits
- Some dependencies may be for notebooks only - could separate those out
