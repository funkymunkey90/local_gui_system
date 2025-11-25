"""Loads and stores settigns found in toml files."""
#-------------------------------------------------
# Imports
#-------------------------------------------------
from threading import Lock
import os
from pathlib import Path
from typing import Any, Union
import tomllib  # Python 3.11+ for reading TOML
import toml     # 3rd-party package for writing TOML
#-------------------------------------------------
# Variables
#-------------------------------------------------

#-------------------------------------------------
# functions
#-------------------------------------------------

def load_setting_toml_files (source_path:str):
    """Loads toml files found in source path."""
    _toml_files = []
    for _root, _dir, _files in os.walk(source_path):
        for _file in _files:
            if _file.endswith('.toml'):
                _toml_files.append(os.path.join(_root, _file))
    for _toml in _toml_files:
        try:
            _label = str(os.path.basename(_toml)).rsplit('.', maxsplit=1)[0]
            Settings_Man.load_file(_label, _toml)
        except Exception as e:
            raise FileNotFoundError (f"Settings - Unable to load file: '{_toml}'") from e

#-------------------------------------------------
# classes
#-------------------------------------------------

class SettingsManager:
    """Manages loaded settings"""
    _instance = None
    _lock = Lock()
    _config_data:dict[str,Any] = {}
    _file_paths:dict[str,Any] = {}
    _placeholders:dict[str,Any] = {}

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(SettingsManager, cls).__new__(cls)
                cls._instance._config_data = {}
                cls._instance._file_paths = {}
                cls._instance._placeholders = {
                    "{main_root}":os.getcwd()
                }
        return cls._instance
    
    def load_file(self, label: str, file_path: str):
        """
        Loads a TOML file and stores it under a label for reference.
        """
        file = Path(file_path)
        if not file.exists():
            raise FileNotFoundError(f"TOML file '{file_path}' not found.")

        with open(file, "rb") as f:
            config = tomllib.load(f)
        
        config = self._replace_placeholders(config)
        
        self._config_data[label] = config
        self._file_paths[label] = file
        

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieves a nested config value using dot notation.
        Example: get("database.host")
        """
        parts = key.split(".")
        for config in self._config_data.values():
            current = config
            for part in parts:
                if isinstance(current, dict) and part in current:
                    current = current[part]
                else:
                    break
            else:
                return current  # Return only if all parts matched
        return default

    def set(self, key: str, value: Any, label: str):
        """
        Sets a nested value in a specific labeled config.
        Example: set("server.port", 8080, label="main")
        """
        if label not in self._config_data:
            raise IndexError (f"No config loaded under label '{label}'.")

        parts = key.split(".")
        current = self._config_data[label]
        for part in parts[:-1]:
            current = current.setdefault(part, {})

        current[parts[-1]] = value

    def save(self, label: str):
        """
        Saves the specified labeled config back to its original file.
        """
        if label not in self._config_data or label not in self._file_paths:
            raise IndexError(f"Cannot save config. Unknown label: '{label}'")

        file = self._file_paths[label]
        with open(file, "w", encoding="utf-8") as f:
            toml.dump(self._config_data[label], f)

    def get_all(self) -> dict:
        """
        Returns all currently loaded configuration data.
        """
        return self._config_data
    
    def set_placeholder(self, key: str, value: str):
        """Add or update a placeholder for substitution."""
        self._placeholders[key] = value
    
    def _replace_placeholders(self, data: Union[dict, list, str]) -> Union[dict, list, str]:
        if isinstance(data, dict):
            return {k: self._replace_placeholders(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._replace_placeholders(i) for i in data]
        elif isinstance(data, str):
            for placeholder, actual in self._placeholders.items():
                data = data.replace(placeholder, actual)
            return data
        return data
    
#-------------------------------------------------
# Initilization
#-------------------------------------------------

Settings_Man = SettingsManager()
