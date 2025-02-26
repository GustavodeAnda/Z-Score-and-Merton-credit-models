"""
merton_model.py

This module contains the MertonModel class, which estimates a company's default probability
and optionally its equity value using the Merton model. The Merton model assumes that a company's
equity can be viewed as a call option on its assets, with the debt acting as the strike price.
It uses the Black-Scholes formula to calculate the option value and default probability.

Key formulas:
    d1 = (ln(V/D) + (r + 0.5 * σ^2) * T) / (σ * sqrt(T))
    d2 = d1 - σ * sqrt(T)
    
    Equity (call option value): C = V * N(d1) - D * exp(-r * T) * N(d2)
    Default Probability: PD = N(-d2)

where:
    V = Asset value
    D = Debt (face value)
    σ = Volatility of the asset value
    r = Risk-free interest rate
    T = Time to maturity (in years)
"""

import math
from scipy.stats import norm

class MertonModel:
    def __init__(self, asset_value: float, debt: float, volatility: float,
                 risk_free_rate: float, time_to_maturity: float):
        """
        Initializes the MertonModel with the necessary parameters.
        
        :param asset_value: Current value of the company's assets (V).
        :param debt: Total debt or face value of debt (D).
        :param volatility: Volatility of the asset value (σ), expressed as a decimal.
        :param risk_free_rate: Risk-free interest rate (r), expressed as a decimal.
        :param time_to_maturity: Time to maturity (T) in years.
        """
        self.asset_value = asset_value
        self.debt = debt
        self.volatility = volatility
        self.risk_free_rate = risk_free_rate
        self.time_to_maturity = time_to_maturity
        self.default_probability = None
        self.equity_value = None

    def calculate(self) -> dict:
        """
        Calculates the default probability and the equity value using the Merton model.

        The calculations are as follows:
            d1 = (ln(V/D) + (r + 0.5 * volatility^2) * T) / (volatility * sqrt(T))
            d2 = d1 - volatility * sqrt(T)
            
            Equity (call option value) = V * N(d1) - D * exp(-r * T) * N(d2)
            Default Probability = N(-d2)

        :return: A dictionary with the keys 'default_probability' and 'equity_value'.
        """
        try:
            # Calculate d1 and d2
            d1 = (math.log(self.asset_value / self.debt) + 
                  (self.risk_free_rate + 0.5 * self.volatility ** 2) * self.time_to_maturity) / \
                  (self.volatility * math.sqrt(self.time_to_maturity))
            d2 = d1 - self.volatility * math.sqrt(self.time_to_maturity)

            # Calculate equity as the call option value
            self.equity_value = (self.asset_value * norm.cdf(d1) -
                                 self.debt * math.exp(-self.risk_free_rate * self.time_to_maturity) * norm.cdf(d2))

            # Calculate default probability as the probability that asset value falls below debt at maturity
            self.default_probability = norm.cdf(-d2)

        except Exception as e:
            print(f"Error in Merton model calculation: {e}")
            self.default_probability = None
            self.equity_value = None

        return {
            'default_probability': self.default_probability,
            'equity_value': self.equity_value
        }

if __name__ == "__main__":
    # Example usage:
    # Sample values to demonstrate functionality
    # Assume: asset_value = $1,000,000, debt = $800,000, volatility = 20%,
    # risk_free_rate = 5% and time_to_maturity = 1 year.
    merton = MertonModel(
        asset_value=1_000_000,
        debt=800_000,
        volatility=0.20,
        risk_free_rate=0.05,
        time_to_maturity=1
    )
    results = merton.calculate()
    if results['default_probability'] is not None:
        print(f"Calculated Equity Value: ${results['equity_value']:.2f}")
        print(f"Default Probability: {results['default_probability']:.2%}")
    else:
        print("Failed to calculate Merton model results.")
