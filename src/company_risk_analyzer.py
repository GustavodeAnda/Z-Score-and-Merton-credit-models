"""
company_risk_analyzer.py

This module integrates the analysis of credit risk using both the Altman Z-Score and the Merton Model.
It defines the CompanyRiskAnalyzer class, which uses data from Yahoo Finance (via yfinance) to extract
financial metrics and compute risk measures.

Features:
    - Automatic extraction of financial values (with flexible key matching).
    - Calculation of Altman Z-Score.
    - Calculation of annualized equity volatility.
    - Calculation of default probability using the Merton Model.
    - Simple credit decision based on thresholds.
    - Allows the user to input any number of tickers and an optional date range for historical data.
"""

import yfinance as yf
import pandas as pd
import numpy as np
import math
from scipy.stats import norm

class CompanyRiskAnalyzer:
    def __init__(self, ticker, start_date: str = None, end_date: str = None):
        """
        Initializes the analyzer with a ticker symbol.

        :param ticker: The ticker symbol of the company (e.g., "AAPL").
        :param start_date: Optional start date (YYYY-MM-DD) for historical data.
        :param end_date: Optional end date (YYYY-MM-DD) for historical data.
        """
        self.ticker_symbol = ticker
        self.ticker = yf.Ticker(ticker)
        self.balance_sheet = self.ticker.balance_sheet
        self.income_statement = self.ticker.financials
        self.info = self.ticker.info

        # Use DataLoader if dates are provided; otherwise, fallback to default 1-year history.
        if start_date and end_date:
            try:
                from data_loader import DataLoader
                loader = DataLoader()
                self.history = loader.get_financial_data(ticker, start_date, end_date)
            except Exception as e:
                print(f"Error using DataLoader: {e}")
                self.history = self.ticker.history(period="1y")
        else:
            self.history = self.ticker.history(period="1y")
        
        # Debug prints removed.
        # print(f"Balance sheet keys for {ticker}: {self.balance_sheet.index.tolist()}")
        # print(f"Income statement keys for {ticker}: {self.income_statement.index.tolist()}")

    def get_financial_value(self, df, key_list):
        """
        Searches for the first key available in key_list within DataFrame df (case-insensitive).

        :param df: Pandas DataFrame containing financial data.
        :param key_list: List of possible key names.
        :return: The value corresponding to the first found key or None.
        """
        for key in key_list:
            for k in df.index:
                if k.lower() == key.lower():
                    return df.loc[k].iloc[0]
        return None

    def calculate_altman_z_score(self):
        """
        Calculates the Altman Z-Score using automatically extracted financial values.
        
        :return: The Altman Z-Score or None if required data is missing.
        """
        # Attempt to obtain Working Capital directly.
        working_capital = self.get_financial_value(self.balance_sheet, ["Working Capital", "workingCapital", "Total Working Capital"])
        # If not found, calculate as Current Assets - Current Liabilities.
        if working_capital is None:
            current_assets = self.get_financial_value(self.balance_sheet, ["Total Current Assets", "currentAssets", "Current Assets"])
            current_liabilities = self.get_financial_value(self.balance_sheet, ["Total Current Liabilities", "currentLiabilities", "Current Liabilities"])
            if current_assets is not None and current_liabilities is not None:
                working_capital = current_assets - current_liabilities

        total_assets = self.get_financial_value(self.balance_sheet, ["Total Assets", "totalAssets"])
        total_liabilities = self.get_financial_value(self.balance_sheet, [
            "Total Liab", "Total Liabilities", "totalLiab", "totalLiabilities", 
            "Total Liabilities Net Minority Interest"
        ])
        retained_earnings = self.get_financial_value(self.balance_sheet, ["Retained Earnings", "retainedEarnings"])
        ebit = self.get_financial_value(self.income_statement, ["Ebit", "EBIT", "Operating Income", "operatingIncome"])
        revenue = self.get_financial_value(self.income_statement, ["Total Revenue", "totalRevenue", "Revenue"])
        market_cap = self.info.get("marketCap", None)
        
        # Verify that all necessary data has been obtained.
        if None in [total_assets, total_liabilities, working_capital, retained_earnings, ebit, revenue, market_cap]:
            print(f"Missing data to calculate Altman Z-score for {self.ticker_symbol}")
            return None
        
        X1 = working_capital / total_assets
        X2 = retained_earnings / total_assets
        X3 = ebit / total_assets
        X4 = market_cap / total_liabilities
        X5 = revenue / total_assets
        
        Z = 1.2 * X1 + 1.4 * X2 + 3.3 * X3 + 0.6 * X4 + 1.0 * X5
        return Z

    def calculate_equity_volatility(self):
        """
        Calculates annualized volatility based on daily return data.
        
        :return: Annualized volatility, or a default value if historical data is missing.
        """
        if self.history is None or self.history.empty:
            return 0.3  # Default value.
        daily_returns = self.history['Close'].pct_change().dropna()
        volatility = daily_returns.std() * np.sqrt(252)
        return volatility

    def calculate_merton_default_probability(self, sigma=None, T=1):
        """
        Calculates the default probability using the Merton Model.
        
        :param sigma: Optional; volatility value. If not provided, calculated from equity volatility.
        :param T: Time to maturity (in years). Default is 1.
        :return: The default probability (as a decimal) or None if required data is missing.
        """
        total_liabilities = self.get_financial_value(self.balance_sheet, [
            "Total Liab", "Total Liabilities", "totalLiab", "totalLiabilities", 
            "Total Liabilities Net Minority Interest"
        ])
        market_cap = self.info.get("marketCap", None)
        
        if None in [total_liabilities, market_cap]:
            print(f"Missing data for Merton Model in {self.ticker_symbol}")
            return None
        
        V = market_cap + total_liabilities
        D = total_liabilities
        
        if sigma is None:
            sigma = self.calculate_equity_volatility()
        
        d2 = (math.log(V / D) - 0.5 * sigma**2 * T) / (sigma * math.sqrt(T))
        default_prob = norm.cdf(-d2)
        return default_prob

    def credit_decision(self, z_score, default_prob):
        """
        Provides a simple credit decision:
          - "Aprobado" if Z-score >= 3 and default_prob < 5%
          - "Denegado" otherwise or if data is insufficient.
        
        :param z_score: Calculated Altman Z-Score.
        :param default_prob: Calculated Merton default probability.
        :return: A string indicating the credit decision.
        """
        if z_score is None or default_prob is None:
            return "Datos insuficientes"
        if z_score >= 3 and default_prob < 0.05:
            return "Aprobado"
        else:
            return "Denegado"

def main():
    print("Welcome to the Credit Risk Analysis using Altman Z-Score and Merton Model!")
    
    # Request tickers from the user, separated by commas.
    tickers_input = input("Please enter ticker symbols separated by commas (e.g., AAPL, MSFT, GOOGL): ")
    tickers = [ticker.strip() for ticker in tickers_input.split(",") if ticker.strip() != ""]
    
    # Optional: Request historical date range.
    start_date = input("Enter the start date (YYYY-MM-DD) for historical data (leave blank for default 1 year): ").strip()
    end_date = input("Enter the end date (YYYY-MM-DD) for historical data (leave blank for default 1 year): ").strip()
    if start_date == "" or end_date == "":
        start_date = None
        end_date = None

    results = []
    
    for ticker in tickers:
        analyzer = CompanyRiskAnalyzer(ticker, start_date, end_date)
        z_score = analyzer.calculate_altman_z_score()
        default_prob = analyzer.calculate_merton_default_probability()
        decision = analyzer.credit_decision(z_score, default_prob)
        results.append({
            "Ticker": ticker,
            "Altman Z-Score": z_score,
            "Merton PD": default_prob,  # Numeric value
            "Credit Decision": decision
        })
    
    df_results = pd.DataFrame(results)
    # Format the default probability as percentage.
    if not df_results.empty:
        df_results["Merton PD"] = df_results["Merton PD"].apply(
            lambda x: f"{(x.item() * 100):.2f}%" if (x is not None and hasattr(x, "item")) else (f"{x * 100:.2f}%" if x is not None else "N/A")
        )
    
    print("\nCredit Risk Analysis Results:")
    print(df_results)
    return df_results

if __name__ == "__main__":
    main()
