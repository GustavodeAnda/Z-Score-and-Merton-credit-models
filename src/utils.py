"""
utils.py

This module contains utility functions used in the Credit Risk Analysis project.

Functions:
    - calculate_ratios: Calculates the financial ratios required for the Altman Z-Score.
    - black_scholes: Computes the European call option price using the Black-Scholes formula.
    - plot_credit_results_df: Plots a grouped bar chart to visually display credit risk metrics.
"""

import math
from typing import Dict
from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np

def calculate_ratios(working_capital: float, retained_earnings: float, ebit: float,
                     total_assets: float, market_value_equity: float, total_liabilities: float,
                     sales: float) -> Dict[str, float]:
    """
    Calculates the financial ratios required for the Altman Z-Score calculation.
    
    Ratios computed:
        ratio1 = Working Capital / Total Assets
        ratio2 = Retained Earnings / Total Assets
        ratio3 = EBIT / Total Assets
        ratio4 = Market Value of Equity / Total Liabilities
        ratio5 = Sales / Total Assets
    
    :param working_capital: Company's working capital.
    :param retained_earnings: Company's retained earnings.
    :param ebit: Earnings before interest and taxes.
    :param total_assets: Total assets of the company.
    :param market_value_equity: Market value of the company's equity.
    :param total_liabilities: Total liabilities of the company.
    :param sales: Company's sales.
    :return: A dictionary containing the calculated ratios.
    :raises ValueError: If total_assets or total_liabilities is zero.
    """
    try:
        ratio1 = working_capital / total_assets
        ratio2 = retained_earnings / total_assets
        ratio3 = ebit / total_assets
        ratio4 = market_value_equity / total_liabilities
        ratio5 = sales / total_assets
    except ZeroDivisionError:
        raise ValueError("Total assets and total liabilities must be non-zero.")

    return {
        "working_capital_ratio": ratio1,
        "retained_earnings_ratio": ratio2,
        "ebit_ratio": ratio3,
        "equity_liability_ratio": ratio4,
        "sales_ratio": ratio5
    }

def black_scholes(S: float, K: float, T: float, r: float, sigma: float) -> float:
    """
    Calculates the European call option price using the Black-Scholes formula.
    
    Formulas:
        d1 = (ln(S/K) + (r + 0.5 * sigma^2) * T) / (sigma * sqrt(T))
        d2 = d1 - sigma * sqrt(T)
        
        Call Price = S * N(d1) - K * exp(-r * T) * N(d2)
    
    :param S: Current stock price.
    :param K: Strike price.
    :param T: Time to maturity in years.
    :param r: Risk-free interest rate (as a decimal).
    :param sigma: Volatility of the underlying asset (as a decimal).
    :return: The calculated European call option price.
    :raises ValueError: If an error occurs during calculation.
    """
    try:
        d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)
        call_price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
        return call_price
    except Exception as e:
        raise ValueError(f"Error in Black-Scholes calculation: {e}")

def plot_credit_results_df(df):
    """
    Plots a grouped bar chart for credit risk results from a DataFrame.
    
    The DataFrame must contain the following columns:
        - "Ticker": Company ticker.
        - "Altman Z-Score": Numeric Altman Z-Score.
        - "Merton PD": Numeric Merton Default Probability (decimal).
    
    :param df: DataFrame with the credit risk analysis results.
    """
    required_columns = {"Ticker", "Altman Z-Score", "Merton PD"}
    if not required_columns.issubset(df.columns):
        print("DataFrame must contain 'Ticker', 'Altman Z-Score' and 'Merton PD' columns.")
        return

    tickers = df["Ticker"].tolist()
    altman_scores = df["Altman Z-Score"].tolist()
    merton_pd_pct = [val * 100 for val in df["Merton PD"].tolist()]
    
    x = np.arange(len(tickers))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    bars1 = ax.bar(x - width/2, altman_scores, width, label="Altman Z-Score", color='skyblue')
    bars2 = ax.bar(x + width/2, merton_pd_pct, width, label="Merton Default Prob. (%)", color='lightcoral')

    ax.set_ylabel("Value")
    ax.set_title("Credit Risk Analysis Results by Ticker")
    ax.set_xticks(x)
    ax.set_xticklabels(tickers)
    ax.legend()

    def autolabel(bars):
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(bars1)
    autolabel(bars2)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Example usage:
    import pandas as pd
    data = {
        "Ticker": ["AAPL", "MSFT", "GOOGL"],
        "Altman Z-Score": [2.8, 3.5, 2.1],
        "Merton PD": [0.04, 0.03, 0.08]
    }
    df_example = pd.DataFrame(data)
    plot_credit_results_df(df_example)
