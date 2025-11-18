# Issue: Environment Configuration

**Priority**: Low
**Category**: Configuration
**Estimated Effort**: Small (2-3 hours)
**Can be parallelized**: Yes (independent task)

## Description

The project uses environment variables for API keys but lacks:
- `.env.example` template file
- Documentation of all required variables
- Validation of environment variables at startup
- Clear error messages when variables are missing

## Current State

- ✅ Uses python-dotenv for loading .env files
- ✅ README documents .env file usage
- ✅ `.env` is in .gitignore (assumed)
- ❌ No `.env.example` template
- ❌ No comprehensive list of all env variables
- ❌ Error handling in load_llm_env() only checks LLM keys
- ❌ No validation for other potential env variables

## Proposed Solution

### 1. Create `.env.example` Template

Create `.env.example` in repository root:
```bash
# LLM API Keys
OPENAI_API_KEY=sk-your-openai-api-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-api-key-here

# UN Comtrade API
# Get your key from: https://comtradeapi.un.org/
COMTRADE_API_KEY=your-comtrade-api-key-here

# Optional: EIA API (Energy Information Administration)
# Get your key from: https://www.eia.gov/opendata/register.php
EIA_API_KEY=your-eia-api-key-here

# Optional: Google Sheets API
# Set up at: https://console.cloud.google.com/
GOOGLE_SHEETS_CREDENTIALS_PATH=/path/to/credentials.json

# Application Settings
LOG_LEVEL=INFO
DEBUG_MODE=false
DATA_DIR=./data
```

### 2. Improve Environment Variable Loading

Create a new `src/bizwiz/config.py`:
```python
"""Configuration management for bizwiz."""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)


class ConfigError(Exception):
    """Raised when required configuration is missing."""
    pass


class Config:
    """Application configuration loaded from environment variables."""

    def __init__(self, env_file: Optional[str] = None):
        """Load configuration from environment.

        Args:
            env_file: Path to .env file. If None, uses default .env

        Raises:
            ConfigError: If required variables are missing
        """
        load_dotenv(env_file)
        self._validate()

    def _validate(self) -> None:
        """Validate that required environment variables are set."""
        errors = []

        # Check LLM API keys (at least one required)
        if not self.openai_api_key and not self.anthropic_api_key:
            errors.append(
                "At least one LLM API key required: "
                "OPENAI_API_KEY or ANTHROPIC_API_KEY"
            )

        if errors:
            error_msg = "Configuration errors:\n" + "\n".join(f"  - {e}" for e in errors)
            raise ConfigError(error_msg)

    # LLM API Keys
    @property
    def openai_api_key(self) -> Optional[str]:
        """OpenAI API key."""
        return os.getenv('OPENAI_API_KEY')

    @property
    def anthropic_api_key(self) -> Optional[str]:
        """Anthropic API key."""
        return os.getenv('ANTHROPIC_API_KEY')

    # Data API Keys
    @property
    def comtrade_api_key(self) -> Optional[str]:
        """UN Comtrade API key."""
        key = os.getenv('COMTRADE_API_KEY')
        if not key:
            logger.warning(
                "COMTRADE_API_KEY not set. "
                "Trade data functions will not work. "
                "Get a key from https://comtradeapi.un.org/"
            )
        return key

    @property
    def eia_api_key(self) -> Optional[str]:
        """EIA API key for energy data."""
        return os.getenv('EIA_API_KEY')

    # Application Settings
    @property
    def log_level(self) -> str:
        """Logging level."""
        return os.getenv('LOG_LEVEL', 'INFO')

    @property
    def debug_mode(self) -> bool:
        """Debug mode flag."""
        return os.getenv('DEBUG_MODE', 'false').lower() == 'true'

    @property
    def data_dir(self) -> Path:
        """Data directory path."""
        return Path(os.getenv('DATA_DIR', './data'))


# Global config instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get or create global config instance."""
    global _config
    if _config is None:
        _config = Config()
    return _config


def load_config(env_file: Optional[str] = None) -> Config:
    """Load configuration from environment file.

    Args:
        env_file: Path to .env file

    Returns:
        Config instance

    Example:
        >>> config = load_config('.env.dev')
        >>> api_key = config.anthropic_api_key
    """
    global _config
    _config = Config(env_file)
    return _config
```

### 3. Update llm.py to Use New Config

```python
from .config import get_config

def load_llm_env(llm_vendors: list[str] | None = None) -> bool:
    """Load and validate LLM environment variables.

    Args:
        llm_vendors: Optional list of vendors to validate (deprecated)

    Returns:
        True if configuration is valid

    Raises:
        ConfigError: If required variables are missing
    """
    try:
        config = get_config()
        return True
    except ConfigError as e:
        raise KeyError(str(e))


class ChatManager:
    """Manage chat interactions with LLMs."""

    def __init__(self, temperature: float = 0.0):
        # Load config
        config = get_config()

        # Initialize client
        if config.anthropic_api_key:
            self.client = anthropic.Client(api_key=config.anthropic_api_key)
        else:
            raise ValueError("ANTHROPIC_API_KEY not configured")

        # ... rest of init
```

### 4. Add Configuration Documentation

Create `docs/configuration.md`:
```markdown
# Configuration

BizWiz uses environment variables for configuration.

## Quick Start

1. Copy the example file:
   \```bash
   cp .env.example .env
   \```

2. Edit `.env` and add your API keys

3. Run your code - configuration is loaded automatically

## Required Variables

### LLM API Keys

At least one LLM API key is required:

- **OPENAI_API_KEY**: OpenAI API key ([Get one](https://platform.openai.com/api-keys))
- **ANTHROPIC_API_KEY**: Anthropic API key ([Get one](https://console.anthropic.com/))

### Trade Data

- **COMTRADE_API_KEY**: UN Comtrade API key ([Get one](https://comtradeapi.un.org/))

## Optional Variables

- **EIA_API_KEY**: Energy Information Administration API key
- **LOG_LEVEL**: Logging level (default: INFO)
- **DEBUG_MODE**: Enable debug mode (default: false)
- **DATA_DIR**: Path to data directory (default: ./data)

## Environment Files

You can use different `.env` files for different environments:

\```python
from bizwiz.config import load_config

# Development
config = load_config('.env.dev')

# Production
config = load_config('.env.prod')
\```

## Validation

Configuration is validated on load. Clear error messages will indicate missing required variables.
```

### 5. Add to .gitignore

Ensure `.env` is ignored but `.env.example` is tracked:
```gitignore
# Environment files
.env
.env.local
.env.*.local

# But not the example
!.env.example
```

### 6. Update README

Add to README.md:
```markdown
## Configuration

1. Copy the example environment file:
   \```bash
   cp .env.example .env
   \```

2. Edit `.env` and add your API keys:
   - Get Anthropic API key: https://console.anthropic.com/
   - Get Comtrade API key: https://comtradeapi.un.org/

See [docs/configuration.md](docs/configuration.md) for full details.
```

## Acceptance Criteria

- [ ] `.env.example` created with all variables documented
- [ ] New `config.py` module with Config class
- [ ] Clear error messages for missing required variables
- [ ] Warnings for missing optional variables
- [ ] Documentation of all environment variables
- [ ] `.gitignore` properly configured
- [ ] README updated with configuration instructions

## Dependencies

- None (can start immediately)

## Related Issues

- #03-documentation-improvements (configuration docs)

## Implementation Steps

1. Create `.env.example` with all variables
2. Create `src/bizwiz/config.py`
3. Update `src/bizwiz/llm.py` to use new config
4. Create `docs/configuration.md`
5. Update .gitignore if needed
6. Update README with configuration section
7. Test configuration loading and validation

## Notes

- Clear error messages save developer time
- `.env.example` serves as documentation
- Validation prevents runtime errors from missing config
- Consider using pydantic-settings for more advanced config management
