"""Handles all web scraping actions"""
#-------------------------------------------------
# Imports
#-------------------------------------------------
import os
import json
import csv
#import pandas as pd
from typing import Any
from datetime import datetime
import requests
import yfinance as yf
import wikipedia
#import nasdaqdatalink as ndl
from bs4 import BeautifulSoup
from settings_manager import Settings_Man
#-------------------------------------------------
# Variables
#-------------------------------------------------

#-------------------------------------------------
# functions
#-------------------------------------------------

#-------------------------------------------------
# classes
#-------------------------------------------------

class SourceDataScraperManager:
    """Manages scraping data from web sources"""
    _instance:Any = None
    stock_data_dir:str
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SourceDataScraperManager, cls).__new__(cls)
            cls._instance._init()
        return cls._instance
    
    def _init (self):
        self.stock_data_dir = Settings_Man.get("paths.folder_storage")
        if self.stock_data_dir is not None:
            self.set_output_dir(self.stock_data_dir)
        
    def set_output_dir (self, output_dir:str):
        """defines the outp;ut directory"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        self.stock_data_dir = output_dir

    def _save_to_file(self, query, data, directory):

        def _sanitize_filename(query):
            return "".join(c if c.isalnum() else "_" for c in query)

        filename = f"{_sanitize_filename(query)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(directory, filename)
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[✔] Search result saved to {filepath}")
        except IOError as e:
            print(f"[!] Failed to save metadata for {query}: {e}")

    def get_sp500_symbols_to_csv (self):
        """Scrapes S&P 500 symbols from Wikipedia."""
        wiki_sp500_page = wikipedia.page('List of S&P 500 companies')
        soup = BeautifulSoup(wiki_sp500_page.html(), 'html.parser')
        table = soup.find(name="table", attrs={"id":"constituents"})
        headers = []
        rows = []
        if table is not None:
            header_row = table.find('thead')
            if header_row: 
                headers = [th.get_text(strip=True) for th in header_row.find_all('th')]
            else:
                first_row = table.find('tr')
                if first_row:
                    headers = [th.get_text(strip=True) for th in first_row.find_all(['th', 'td'])]
            table_rows = table.find('tbody')
            if table_rows is not None:
                for _r in table_rows.find_all('tr'):
                    cells = _r.find_all('td')
                    if cells:
                        _r_data = {}
                        for _i, header in enumerate(headers):
                            if _i < len(cells):
                                _r_data[header] = cells[_i].get_text(strip=True)
                        rows.append(_r_data)
        filename = f"symbols_SP500_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(Settings_Man.get("paths.folder_storage"), filename)
        with open(filepath, 'w', newline='', encoding="utf-8") as _csvfile:
            writer = csv.DictWriter(_csvfile, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
            
    def get_sp100_symbols_to_csv (self):
        """Scrapes S&P 100 symbols from Wikipedia."""
        wiki_sp500_page = wikipedia.page('S&P 100')
        soup = BeautifulSoup(wiki_sp500_page.html(), 'html.parser')
        table = soup.find(name="table", attrs={"id":"constituents"})
        headers = []
        rows = []
        if table is not None:
            header_row = table.find('thead')
            if header_row: 
                headers = [th.get_text(strip=True) for th in header_row.find_all('th')]
            else:
                first_row = table.find('tr')
                if first_row:
                    headers = [th.get_text(strip=True) for th in first_row.find_all(['th', 'td'])]
            table_rows = table.find('tbody')
            if table_rows is not None:
                for _r in table_rows.find_all('tr'):
                    cells = _r.find_all('td')
                    if cells:
                        _r_data = {}
                        for _i, header in enumerate(headers):
                            if _i < len(cells):
                                _r_data[header] = cells[_i].get_text(strip=True)
                        rows.append(_r_data)
        filename = f"symbols_SP100_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(Settings_Man.get("paths.folder_storage"), filename)
        with open(filepath, 'w', newline='', encoding="utf-8") as _csvfile:
            writer = csv.DictWriter(_csvfile, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
    
    def get_dji_symbols_to_csv (self):
        """Scrapes Dow Jones Industrial symbols from Wikipedia."""
        wiki_sp500_page = wikipedia.page('Dow Jones Industrial Average')
        soup = BeautifulSoup(wiki_sp500_page.html(), 'html.parser')
        table = soup.find(name="table", attrs={"id":"constituents"})
        headers = []
        rows = []
        if table is not None:
            header_row = table.find('thead')
            if header_row: 
                headers = [th.get_text(strip=True) for th in header_row.find_all('th')]
            else:
                first_row = table.find('tr')
                if first_row:
                    headers = [th.get_text(strip=True) for th in first_row.find_all(['th', 'td'])]
            table_rows = table.find('tbody')
            if table_rows is not None:
                for _r in table_rows.find_all('tr'):
                    cells = _r.find_all('td')
                    if cells:
                        _r_data = {}
                        for _i, header in enumerate(headers):
                            if _i < len(cells):
                                _r_data[header] = cells[_i].get_text(strip=True)
                        rows.append(_r_data)
        filename = f"symbols_DJI_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(Settings_Man.get("paths.folder_storage"), filename)
        with open(filepath, 'w', newline='', encoding="utf-8") as _csvfile:
            writer = csv.DictWriter(_csvfile, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
            
    def get_nyse_symbols_to_csv (self):
        """Scrapes NYSE Arca Major Market Index symbols from Wikipedia."""
        wiki_sp500_page = wikipedia.page('NYSE Arca Major Market Index')
        soup = BeautifulSoup(wiki_sp500_page.html(), 'html.parser')
        table = soup.find(name="table", attrs={"class":"wikitable sortable"})
        headers = []
        rows = []
        if table is not None:
            header_row = table.find('thead')
            if header_row: 
                headers = [th.get_text(strip=True) for th in header_row.find_all('th')]
            else:
                first_row = table.find('tr')
                if first_row:
                    headers = [th.get_text(strip=True) for th in first_row.find_all(['th', 'td'])]
            table_rows = table.find('tbody')
            if table_rows is not None:
                for _r in table_rows.find_all('tr'):
                    cells = _r.find_all('td')
                    if cells:
                        _r_data = {}
                        for _i, header in enumerate(headers):
                            if _i < len(cells):
                                _r_data[header] = cells[_i].get_text(strip=True)
                        rows.append(_r_data)
        filename = f"symbols_NYSE_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(Settings_Man.get("paths.folder_storage"), filename)
        with open(filepath, 'w', newline='', encoding="utf-8") as _csvfile:
            writer = csv.DictWriter(_csvfile, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
            
    def search_online_tickers(self, term: str, limit: int = 10, save=True):
        """
        Search Yahoo Finance's public API for ticker symbols related to a search term.
        Saves the result as a JSON file locally.
        """
        _key = Settings_Man.get("keys.key_finnhub")
        if _key is None:
            print ("Unable to find FINNHUB.io API Key")
            return []
        
        url = "https://finnhub.io/api/v1/search"
        params = {
            "q": term,
            "token": _key
        }

        response = requests.get(url=url, params=params, timeout=10)
        if response.status_code != 200:
            print(f"[!] Search failed: {response.status_code}")
            return []

        data = response.json()
        if save:
            self._save_to_file(f"search_{term}", data, self.stock_data_dir)
        
        results = []
        for result in data.get("result", []):
            symbol = result.get("symbol")
            description = result.get("description")
            if symbol and description:
                results.append({"symbol": symbol, "name": description})

        return results[:limit]
        
        
    def get_metadata(self, ticker, save=True):
        """
        Fetch and optionally save ticker metadata.
        """
        stock = yf.Ticker(ticker)
        info = stock.info
        try:
            info = stock.info
        except ValueError as e:
            print(f"[!] Error fetching metadata for {ticker}: {e}")
            return None

        if not isinstance(info, dict) or len(info) <= 1:
            print(f"[!] Empty or invalid metadata for {ticker}: {info}")
            return None
        
        if save:
            self._save_to_file(f"company_{ticker}", info, self.stock_data_dir)
        return info
    
    
    def get_stock_data(self, ticker, period="1mo", interval="1d", fmt="csv"):
        """
        Get historical price data for a ticker and save to file.
        """
        stock = yf.Ticker(ticker)
        try:
            hist = stock.history(period=period, interval=interval)
        except ValueError as e:
            print(f"[!] Failed to fetch history for {ticker}: {e}")
            return None

        if hist.empty:
            print(f"[!] No historical data found for {ticker}")
            return None

        filename = f"candles_{ticker}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{fmt}"
        filepath = os.path.join(self.stock_data_dir, filename)

        try:
            if fmt == "csv":
                hist.to_csv(filepath)
            elif fmt == "json":
                hist.to_json(filepath, orient="records", date_format="iso")
            else:
                raise ValueError("Unsupported format: use 'csv' or 'json'.")
            print(f"[✔] Saved stock data for {ticker} to {filepath}")
            return filepath
        except IOError as e:
            print(f"[!] Failed to save data for {ticker}: {e}")
            return None
    
    
#-------------------------------------------------
# Initilization
#-------------------------------------------------

Source_Web_Scraper = SourceDataScraperManager()
