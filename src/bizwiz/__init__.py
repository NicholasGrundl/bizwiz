"""Python package forCommon business tasks and utilities
"""

# Package meta data (for publishing)
__version__ = (0, 0, 0)
__author__ = "Nick Grundl"
__author_email__ = '"Nick Grundl" <nicholasgrundl@gmail.com>'
__maintainer__ = "Nick Grundl"
__maintainer_email__ = '"Nick Grundl" <nicholasgrundl@gmail.com>'



#default imports

from .data import PathManager
from .llm import load_llm_env, ChatManager
