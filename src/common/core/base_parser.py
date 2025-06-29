import os
import yaml
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod

class BaseConfigParser(ABC):
    """
    Abstract base class for configuration parsers.
    """
    @abstractmethod
    def load(self, config_dir: str, filenames: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Load configuration files from a directory.
        """
        ...

    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieve a configuration by key.
        """
        ...
