"""
utils.py

This module contains utility functions used in the Credit Risk Analysis project.

Functions:
    - calculate_ratios: Calculates the financial ratios required for the Altman Z-Score.
    - black_scholes: Computes the European call option price using the Black-Scholes formula.
"""

import math
from typing import Dict
from scipy.stats import norm

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

if __name__ == "__main__":
    # Example usage for calculate_ratios
    ratios = calculate_ratios(
        working_capital=500000,
        retained_earnings=300000,
        ebit=200000,
        total_assets=1500000,
        market_value_equity=800000,
        total_liabilities=700000,
        sales=1200000
    )
    print("Calculated Ratios for Altman Z-Score:")
    for key, value in ratios.items():
        print(f"{key}: {value:.4f}")
    
    # Example usage for black_scholes
    call_price = black_scholes(
        S=100,    # Current stock price
        K=95,     # Strike price
        T=1,      # Time to maturity (1 year)
        r=0.05,   # Risk-free interest rate (5%)
        sigma=0.2 # Volatility (20%)
    )
    print(f"\nCalculated European Call Option Price: {call_price:.2f}")
