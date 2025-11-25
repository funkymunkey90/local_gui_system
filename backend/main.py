"""Main entry point for backend script"""
#-------------------------------------------------
# Imports
#-------------------------------------------------

import os
import asyncio
from fastapi import FastAPI
#import uvicorn
from .modules import Settings_Man, load_setting_toml_files, convert_symbols_csv_files_to_ticker_list
#from modules.sqlite_manager import SQLite_Man
#from modules.web_scraper_manager import Source_Web_Scraper
#from modules.file_manager import File_Man



#-------------------------------------------------
# Variables
#-------------------------------------------------

script_path = os.path.abspath(__file__)
script_directory = os.path.dirname(script_path)

settings_folder = os.path.join (script_directory, "settings")

my_app = FastAPI()


#-------------------------------------------------
# Functions - async / route callers
#-------------------------------------------------


async def main_tester ():
    """testing"""
    #Source_Web_Scraper.get_DJI_symbols_to_csv()
    #Source_Web_Scraper.get_SP500_symbols_to_csv()
    #Source_Web_Scraper.get_SP100_symbols_to_csv()
    #Source_Web_Scraper.get_NYSE_symbols_to_csv()
    _ticket_list = convert_symbols_csv_files_to_ticker_list(source_path=Settings_Man.get("paths.folder_storage"))
    print (_ticket_list)
    
#-------------------------------------------------
# Initilization
#-------------------------------------------------

if __name__ == "__main__":    
    load_setting_toml_files(settings_folder)    
    
    #SQLite_Man.connect(db_path=os.path.join(Settings_Man.get("paths.folder_data"), Settings_Man.get("paths.database_global_name")))
    
    #uvicorn.run(my_app, host="127.0.0.1", port=8000)
    
    asyncio.run (main_tester())
