"""
data_loader.py

This module contains the DataLoader class, which is responsible for downloading
historical financial data from Yahoo Finance using the yfinance library.

Usage:
    Instantiate DataLoader and call get_financial_data providing the ticker,
    start date, and end date.
"""

import yfinance as yf
import pandas as pd

class DataLoader:
    """
    DataLoader class for retrieving financial data from Yahoo Finance.
    """
    def __init__(self):
        pass

    def get_financial_data(self, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Downloads historical financial data for a given ticker between the specified dates.

        :param ticker: The stock ticker symbol (e.g., 'AAPL').
        :param start_date: The start date for data retrieval in YYYY-MM-DD format.
        :param end_date: The end date for data retrieval in YYYY-MM-DD format.
        :return: A pandas DataFrame containing the financial data. Returns None if no data is found.
        """
        try:
            data = yf.download(ticker, start=start_date, end=end_date, progress=False)
            if data.empty:
                print(f"No data found for {ticker} between {start_date} and {end_date}.")
                return None
            return data
        except Exception as e:
            print(f"Error downloading data for {ticker}: {e}")
            return None

if __name__ == "__main__":
    # Example usage:
    loader = DataLoader()
    ticker = input("Enter ticker (e.g., AAPL): ")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    
    data = loader.get_financial_data(ticker, start_date, end_date)
    if data is not None:
        print(f"Data for {ticker}:")
        print(data.head())
    else:
        print("Failed to download data.")
