"""Handles all files interactions and data conversions"""
#-------------------------------------------------
# Imports
#-------------------------------------------------
import threading
import os
import re
import csv
#from datetime import datetime
from typing import Any
#from concurrent.futures import ThreadPoolExecutor

#from .settings_manager import Settings_Man
from shared_enums import REGEX_patterns
#-------------------------------------------------
# Variables
#-------------------------------------------------

#-------------------------------------------------
# functions
#-------------------------------------------------

#-------------------------------------------------
# classes
#-------------------------------------------------
class FileManager ():
    """Singlton class to handle file interactions"""
    _instance = None
    _lock = threading.Lock()
    _file_paths:list[str]|None = None
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(FileManager, cls).__new__(cls)
                cls._instance._init()
            return cls._instance
    def _init (self):
        self._file_paths = []
    def collect_files (self,
        source_path:str,
        file_names:str|list[str]|None=None,
        formats:str|list[str]|None=None,
        ignore_datatime_stamps:bool = True,
    ) -> list[str]:
        """Collects file in given path, will search all sub directories in source path.
        
        Args:      
            source_path (str | list[str]): path of files to collect.
            file_names (str | list[str]): subtreings to find in file names.
            foramts (str | list[str]): file formats to collect.
        Returns:
            list (str) : list of symbols as strings
        """
        _path:str|None = os.path.abspath(source_path) if os.path.isdir(source_path) else None
        _file_names:list[str]|None = file_names if isinstance(file_names, list) else [file_names] if isinstance(file_names, str) else None
        _file_formats:list[str]|None = formats if isinstance(formats, list) else [formats] if isinstance(formats, str) else None
        if _path is None:
            raise Warning (f"source path provided is not a valid directory path : {source_path}")
        _file_collection:dict[str,list[str]] = {}
        _date_enums_by_priority = [REGEX_patterns.DATE_YEAR_MONTH_DAY, REGEX_patterns.DATE_YEAR_DAY_MONTH, REGEX_patterns.DATE_MONTH_DAY_YEAR, REGEX_patterns.DATE_DAY_MONTH_YEAR, REGEX_patterns.DATE_MONTH_YEAR_DAY, REGEX_patterns.DATE_DAY_YEAR_MONTH]
        for _root, _dirs, _files in os.walk(_path):
            for _file in _files:
                if _file_names is not None and not any([_fn.upper() in _file.upper() for _fn in _file_names]) : 
                    continue
                if _file_formats is not None and not any([_file.lower().endswith(_ff.strip('.').strip('*').lower()) for _ff in _file_formats]) : 
                    continue
                _curr_file_path = os.path.join(_root, _file)
                _relative_path = os.path.relpath(_curr_file_path, source_path)
                _file_name, _file_format = os.path.splitext(_relative_path)
                _file_name_cleaned = _file_name.strip()
                if ignore_datatime_stamps is True:
                    _name_mask:str = _file_name_cleaned
                    _found_date_priority_id:int|None = None
                    _found_span:tuple[int,int]|None = None
                    _found_substring:str|None = None
                    for _priority, _pattern in enumerate(_date_enums_by_priority):
                        _match:re.Match|None = re.search(_pattern, _name_mask, re.IGNORECASE)
                        if _match is not None and _found_date_priority_id is None:
                            _found_date_priority_id = _priority
                            _found_substring = _match.group(0)
                            _found_span = _match.span()
                    if _found_substring is not None and _found_span is not None:
                        _name_mask = _name_mask.replace(_found_substring, '_'*(_found_span[1]-_found_span[0]))
                    _time_match = re.search(REGEX_patterns.TIME_HOUR_MINUTE_SECOND, _name_mask, re.IGNORECASE)
                    if _time_match is not None:
                        _time_span:tuple[int,int] = _time_match.span()
                        _name_mask = _name_mask.replace(_time_match.group(0), '_'*(_time_span[1]-_time_span[0]))
                    _file_name_cleaned = _name_mask.strip('_')
                if _file_name_cleaned in _file_collection:
                    _path_list = [_file_collection[_file_name_cleaned], _curr_file_path]
                    _file_collection[_file_name_cleaned] = _path_list
                else:
                    _file_collection[_file_name_cleaned] = [_curr_file_path]
        _file_paths:list[str] = []
        for _file_list in _file_collection.values():
            for _file_path in _file_list:
                if _file_path not in _file_paths:
                    _file_paths.append(_file_path)
                if self._file_paths is not None and _file_path not in self._file_paths:
                    self._file_paths.append(_file_path)
                    
        return _file_paths
                    
    def open_csv_file (self, source_path:str) -> list[dict[str,Any]]:
        """Opens the source cev file path, and returns a list of names values"""
        _found_rows:list[dict[str,Any]] = []
        if source_path.endswith('csv'):
            with open(source_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    _found_rows.append(row)
        return _found_rows
                
            
        
#-------------------------------------------------
# Initilization
#-------------------------------------------------

File_Man = FileManager()
