"""Manage paths to data and files"""

import pathlib
from typing import Union
import pathlib


PathType = Union[str, pathlib.Path]


class PathManager:
    """Manage paths to data and files"""

    def __init__(self, data_dir: PathType) -> None:
        self._data_dir = None

    #properties
    @property
    def data_dir(self) -> pathlib.Path:
        """Get the path to the data directory"""
        return self._data_dir
    
    @data_dir.setter
    def data_dir(self, path: PathType) -> None:
        self._data_dir = pathlib.Path(path)

    #methods
    def get_data_file(self, filename: PathType ) -> pathlib.Path:
        """Get the path to a file or directory in the data directory
        
        checks that it exists
        """
        
        filepath = self.data_dir / filename
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        return filepath
