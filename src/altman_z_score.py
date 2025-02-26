"""
altman_z_score.py

This module contains the AltmanZScore class, which calculates the Altman Z-Score
to evaluate a company's financial risk.

Formula (for manufacturing companies):
    Z = 1.2 * (Working Capital / Total Assets) +
        1.4 * (Retained Earnings / Total Assets) +
        3.3 * (EBIT / Total Assets) +
        0.6 * (Market Value of Equity / Total Liabilities) +
        1.0 * (Sales / Total Assets)

Note: Ensure you have the necessary financial data for the calculations.
You can obtain these data using the DataLoader module.
"""

class AltmanZScore:
    def __init__(self, working_capital: float, retained_earnings: float, ebit: float,
                 total_assets: float, market_value_equity: float, total_liabilities: float,
                 sales: float):
        """
        Initializes the AltmanZScore class with the required financial data.
        
        :param working_capital: Company's working capital.
        :param retained_earnings: Retained earnings.
        :param ebit: Earnings before interest and taxes.
        :param total_assets: Total assets.
        :param market_value_equity: Market value of equity.
        :param total_liabilities: Total liabilities (debt).
        :param sales: Net sales.
        """
        self.working_capital = working_capital
        self.retained_earnings = retained_earnings
        self.ebit = ebit
        self.total_assets = total_assets
        self.market_value_equity = market_value_equity
        self.total_liabilities = total_liabilities
        self.sales = sales
        self.z_score = None

    def calculate(self) -> float:
        """
        Calculates the Altman Z-Score using the following formula:
        
            Z = 1.2 * (Working Capital / Total Assets) +
                1.4 * (Retained Earnings / Total Assets) +
                3.3 * (EBIT / Total Assets) +
                0.6 * (Market Value of Equity / Total Liabilities) +
                1.0 * (Sales / Total Assets)
        
        :return: The calculated Z-Score value. Returns None if a division by zero occurs.
        """
        try:
            ratio1 = self.working_capital / self.total_assets
            ratio2 = self.retained_earnings / self.total_assets
            ratio3 = self.ebit / self.total_assets
            ratio4 = self.market_value_equity / self.total_liabilities
            ratio5 = self.sales / self.total_assets

            self.z_score = (1.2 * ratio1 +
                            1.4 * ratio2 +
                            3.3 * ratio3 +
                            0.6 * ratio4 +
                            1.0 * ratio5)
        except ZeroDivisionError:
            self.z_score = None
            print("Error: Division by zero encountered during Z-Score calculation.")
        return self.z_score

if __name__ == "__main__":
    # Example usage:
    # Sample values to demonstrate functionality
    altman = AltmanZScore(
        working_capital=500000,
        retained_earnings=300000,
        ebit=200000,
        total_assets=1500000,
        market_value_equity=800000,
        total_liabilities=700000,
        sales=1200000
    )
    z = altman.calculate()
    if z is not None:
        print(f"The calculated Altman Z-Score is: {z:.2f}")
    else:
        print("Could not calculate the Altman Z-Score.")
