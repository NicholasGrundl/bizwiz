# Issue: Notebook Organization and Documentation

**Priority**: Low
**Category**: Organization
**Estimated Effort**: Small (0.5 day)
**Can be parallelized**: Yes (independent task)

## Description

The project has 6 Jupyter notebooks in the `notebooks/` directory that serve as prototypes and examples. However:
- No README explaining what each notebook does
- Unclear naming convention (mix of prefixes)
- No clear workflow or order
- Notebooks may have outdated code
- No notebook testing/validation in CI

## Current State

### Existing Notebooks:
1. `ComTradeSnippets.ipynb` - Comtrade API examples
2. `datacuration-v0.0-eia-api.ipynb` - EIA API integration
3. `datacuration-v0.0-pdf-analyzer.ipynb` - PDF analysis
4. `datacuration-v0.0-screenshot-table-to-csv.ipynb` - Screenshot table extraction
5. `datacuration-v0.0-undata-api.ipynb` - UN Data API
6. `solubility-SolubilityInterpolation.ipynb` - Solubility data interpolation
7. `solubility-TableExtractor.ipynb` - Table extraction

### Issues:
- ❌ No notebooks/README.md explaining each notebook
- ⚠️ Inconsistent naming (some have version prefixes, some don't)
- ❌ No execution order documented
- ❌ May have hardcoded paths
- ❌ No CI validation (notebooks could be broken)

## Proposed Solution

### 1. Create notebooks/README.md

```markdown
# Notebooks

This directory contains Jupyter notebooks demonstrating various features and workflows.

## Getting Started

Start Jupyter Lab:
\```bash
make jupyter
\```

## Notebooks Overview

### Trade Data Analysis

1. **ComTradeSnippets.ipynb**
   - Examples of using the UN Comtrade API
   - Country and commodity code lookups
   - Fetching and processing trade data
   - **Prerequisites**: COMTRADE_API_KEY

### Data Curation

2. **datacuration-v0.0-eia-api.ipynb**
   - Energy Information Administration API integration
   - Fetching electricity price data
   - **Prerequisites**: EIA_API_KEY

3. **datacuration-v0.0-pdf-analyzer.ipynb**
   - Extracting text and data from PDF documents
   - Using LLM for structured data extraction
   - **Prerequisites**: ANTHROPIC_API_KEY

4. **datacuration-v0.0-screenshot-table-to-csv.ipynb**
   - Converting screenshots of tables to CSV
   - Image processing and OCR techniques
   - **Prerequisites**: ANTHROPIC_API_KEY

5. **datacuration-v0.0-undata-api.ipynb**
   - UN Data API integration
   - Fetching statistical data

### Solubility Analysis

6. **solubility-TableExtractor.ipynb**
   - Extracting solubility tables from PDFs
   - Data cleaning and standardization

7. **solubility-SolubilityInterpolation.ipynb**
   - Interpolating solubility curves
   - Visualization and analysis

## Recommended Order

If you're new to the project:
1. Start with `ComTradeSnippets.ipynb` to understand trade data
2. Try `datacuration-v0.0-screenshot-table-to-csv.ipynb` for LLM capabilities
3. Explore `solubility-SolubilityInterpolation.ipynb` for data analysis

## Development Notes

- Notebooks use relative paths from project root
- Ensure .env file is configured before running
- Some notebooks may take time to run due to API calls
- Data files are located in `../data/`

## Contributing

When adding new notebooks:
- Use descriptive names
- Add entry to this README
- Test that notebook runs from clean kernel
- Avoid committing output (use nbstripout)
```

### 2. Standardize Notebook Naming

Consider renaming for consistency:
```
Current → Suggested
-------------------
ComTradeSnippets.ipynb → 01-comtrade-api-examples.ipynb
datacuration-v0.0-eia-api.ipynb → 02-eia-api-integration.ipynb
datacuration-v0.0-pdf-analyzer.ipynb → 03-pdf-data-extraction.ipynb
datacuration-v0.0-screenshot-table-to-csv.ipynb → 04-screenshot-to-csv.ipynb
datacuration-v0.0-undata-api.ipynb → 05-undata-api-integration.ipynb
solubility-TableExtractor.ipynb → 06-solubility-table-extraction.ipynb
solubility-SolubilityInterpolation.ipynb → 07-solubility-interpolation.ipynb
```

Or keep current names and just document them well.

### 3. Add nbstripout for Clean Commits

Install nbstripout to automatically strip notebook outputs:
```bash
pip install nbstripout
nbstripout --install
```

Add to `.gitattributes`:
```
*.ipynb filter=nbstripout
```

Add to requirements-dev.txt:
```
nbstripout
```

### 4. Clean Up Notebooks

For each notebook:
- Remove any hardcoded paths
- Use config/environment variables for API keys
- Add markdown cells explaining each section
- Ensure it runs from clean kernel
- Add error handling
- Remove sensitive information

### 5. Add Notebook Testing (Optional)

Create `.github/workflows/notebooks.yml`:
```yaml
name: Notebook Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.10"
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install nbval pytest
      - name: Test notebooks
        run: |
          # Only test notebooks that don't require API keys
          pytest --nbval notebooks/solubility-*.ipynb
```

### 6. Create Notebook Template

Create `notebooks/_template.ipynb`:
```python
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Notebook Title\n",
    "\n",
    "**Author**: Your Name\n",
    "**Date**: YYYY-MM-DD\n",
    "**Prerequisites**: List any API keys or data files needed\n",
    "\n",
    "## Overview\n",
    "\n",
    "Brief description of what this notebook does.\n",
    "\n",
    "## Setup\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Imports\n",
    "import sys\n",
    "from pathlib import Path\n",
    "\n",
    "# Add src to path\n",
    "project_root = Path.cwd().parent\n",
    "sys.path.insert(0, str(project_root / 'src'))\n",
    "\n",
    "# Import bizwiz modules\n",
    "from bizwiz import PathManager, ChatManager\n",
    "from bizwiz.config import get_config"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# Load configuration\n",
    "config = get_config()\n",
    "# ... rest of setup"
   ]
  }
 ]
}
```

## Acceptance Criteria

- [ ] notebooks/README.md created with all notebooks documented
- [ ] All notebooks tested and working
- [ ] nbstripout configured
- [ ] Hardcoded paths removed
- [ ] API keys loaded from environment
- [ ] Each notebook has explanatory markdown cells
- [ ] (Optional) Notebook names standardized
- [ ] (Optional) Notebook testing in CI

## Dependencies

- **Recommended**: #09-environment-configuration (for loading API keys properly)

## Related Issues

- #03-documentation-improvements

## Implementation Steps

1. Create notebooks/README.md
2. Test each notebook from clean kernel
3. Clean up notebooks (remove hardcoded values)
4. Add explanatory markdown cells
5. Install and configure nbstripout
6. (Optional) Rename notebooks for consistency
7. (Optional) Add notebook testing to CI
8. Create notebook template

## Notes

- Notebooks are great for prototyping and documentation
- nbstripout prevents git diffs on output cells
- Keep notebooks focused - one concept per notebook
- Notebooks can serve as integration tests
- Consider using papermill for parameterized notebook execution
