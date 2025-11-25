"""Collection of schared actions that can be called from anwere in the ssytem"""
#-------------------------------------------------
# Imports
#-------------------------------------------------
from typing import Any
from settings_manager import Settings_Man
from file_manager import File_Man
#from shared_enums import REGEX_patterns
#-------------------------------------------------
# Variables
#-------------------------------------------------

#-------------------------------------------------
# functions
#-------------------------------------------------

def convert_symbols_csv_files_to_ticker_list (source_path:str) -> list[str]:
    """Returns a list of ticker symbols found in *.csv files from teh provided source path"""
    _found_symbols:list[str] = []
    _file_list:list[str] = File_Man.collect_files (
        source_path= source_path or Settings_Man.get("paths.folder_storage"),
        file_names=['symbols'],
        formats=['csv'],
        ignore_datatime_stamps = True
    )
    _col_list:list[str] = ['Symbol']
    for _path in _file_list:
        _found_rows:list[dict[str,Any]] = File_Man.open_csv_file(_path)
        for _row in _found_rows:
            for _col in _col_list:
                if _col in _row.keys() and _row[_col] not in _found_symbols:
                    _found_symbols.append(_row[_col])
    return _found_symbols

#-------------------------------------------------
# classes
#-------------------------------------------------
