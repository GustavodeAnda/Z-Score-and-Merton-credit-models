"""
main.py

Main entry point for the Credit Risk Analysis project using both the Altman Z-Score and Merton Model.

This script:
- Prompts the user for a ticker symbol and a date range.
- Downloads historical stock data using the DataLoader module.
- Automatically fetches the necessary financial metrics from the company's financial statements via yfinance.
- Calculates and displays the Altman Z-Score.
- Calculates and displays the Merton Model's equity value and default probability.
- Evaluates risk using the RiskEvaluator.
"""

import yfinance as yf
import pandas as pd
from data_loader import DataLoader
from altman_z_score import AltmanZScore
from merton_model import MertonModel
from risk_evaluator import RiskEvaluator

def main():
    print("Welcome to the Credit Risk Analysis using Altman Z-Score and Merton Model!")
    
    # Solicita al usuario el ticker y el rango de fechas para la descarga de datos históricos
    ticker_input = input("Enter the ticker symbol (e.g., AAPL): ")
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")
    
    # Descarga de datos históricos usando DataLoader
    loader = DataLoader()
    historical_data = loader.get_financial_data(ticker_input, start_date, end_date)
    if historical_data is not None:
        print(f"\nHistorical data for {ticker_input}:")
        print(historical_data.head())
    else:
        print("Failed to retrieve historical data.")
    
    # Crear un objeto Ticker de yfinance para extraer los estados financieros
    tkr = yf.Ticker(ticker_input)
    
    # Obtener el balance y el estado de resultados (tomando el periodo más reciente)
    balance_sheet = tkr.balance_sheet
    income_statement = tkr.financials

    if balance_sheet.empty:
        print("Balance sheet data not available.")
        return
    if income_statement.empty:
        print("Income statement data not available.")
        return

    bs_col = balance_sheet.columns[0]  # Periodo más reciente
    is_col = income_statement.columns[0] # Periodo más reciente

    # Extracción automática de métricas financieras para el Altman Z-Score

    # Working Capital: intentamos con "Total Current Assets" y "Current Assets", y lo mismo para liabilities.
    try:
        if "Total Current Assets" in balance_sheet.index:
            current_assets = balance_sheet.loc["Total Current Assets", bs_col]
        elif "Current Assets" in balance_sheet.index:
            current_assets = balance_sheet.loc["Current Assets", bs_col]
        else:
            raise KeyError("Current Assets not found")

        if "Total Current Liabilities" in balance_sheet.index:
            current_liabilities = balance_sheet.loc["Total Current Liabilities", bs_col]
        elif "Current Liabilities" in balance_sheet.index:
            current_liabilities = balance_sheet.loc["Current Liabilities", bs_col]
        else:
            raise KeyError("Current Liabilities not found")
            
        working_capital = float(current_assets - current_liabilities)
    except Exception as e:
        print(f"Error fetching Working Capital: {e}")
        working_capital = 1.0  # Valor por defecto

    try:
        retained_earnings = float(balance_sheet.loc["Retained Earnings", bs_col])
    except Exception as e:
        print(f"Error fetching Retained Earnings: {e}")
        retained_earnings = 1.0  # Valor por defecto

    try:
        if "Operating Income" in income_statement.index:
            ebit = float(income_statement.loc["Operating Income", is_col])
        else:
            ebit = float(income_statement.loc["EBIT", is_col])
    except Exception as e:
        print(f"Error fetching EBIT: {e}")
        ebit = 1.0  # Valor por defecto

    try:
        total_assets = float(balance_sheet.loc["Total Assets", bs_col])
    except Exception as e:
        print(f"Error fetching Total Assets: {e}")
        total_assets = 1.0  # Valor por defecto

    try:
        market_value_equity = float(tkr.info.get("marketCap", 1))
    except Exception as e:
        print(f"Error fetching Market Value of Equity: {e}")
        market_value_equity = 1.0  # Valor por defecto

    try:
        if "Total Liab" in balance_sheet.index:
            total_liabilities = balance_sheet.loc["Total Liab", bs_col]
        elif "Liabilities" in balance_sheet.index:
            total_liabilities = balance_sheet.loc["Liabilities", bs_col]
        else:
            raise KeyError("Liabilities not found")
        total_liabilities = float(total_liabilities)
    except Exception as e:
        print(f"Error fetching Total Liabilities: {e}")
        total_liabilities = 1.0  # Valor por defecto

    try:
        if "Total Revenue" in income_statement.index:
            sales = float(income_statement.loc["Total Revenue", is_col])
        else:
            sales = 1.0
    except Exception as e:
        print(f"Error fetching Sales: {e}")
        sales = 1.0  # Valor por defecto

    # Cálculo automático del Altman Z-Score
    altman = AltmanZScore(
        working_capital, retained_earnings, ebit,
        total_assets, market_value_equity, total_liabilities, sales
    )
    z_score = altman.calculate()
    if z_score is not None:
        print(f"\nCalculated Altman Z-Score: {z_score:.2f}")
    else:
        print("\nFailed to calculate Altman Z-Score.")
    
    # Extracción automática de parámetros para el Modelo de Merton
    try:
        asset_value = total_assets  # Usamos Total Assets como proxy
    except Exception as e:
        print(f"Error fetching Asset Value: {e}")
        asset_value = 40.0

    try:
        if "Short Term Debt" in balance_sheet.index and "Long Term Debt" in balance_sheet.index:
            debt = float(balance_sheet.loc["Short Term Debt", bs_col] + balance_sheet.loc["Long Term Debt", bs_col])
        elif "Long Term Debt" in balance_sheet.index:
            debt = float(balance_sheet.loc["Long Term Debt", bs_col])
        else:
            debt = 40.0
    except Exception as e:
        print(f"Error fetching Debt: {e}")
        debt = 40.0

    try:
        returns = historical_data["Close"].pct_change().dropna()
        vol_value = returns.std()
        # Para evitar el FutureWarning: convertir usando .iloc[0] si es una Serie de un solo elemento
        if hasattr(vol_value, 'iloc'):
            vol_value = float(vol_value.iloc[0])
        else:
            vol_value = float(vol_value)
        volatility = vol_value * (252 ** 0.5)
    except Exception as e:
        print(f"Error calculating Volatility: {e}")
        volatility = 0.2

    risk_free_rate = 0.05  # Valor por defecto
    time_to_maturity = 5   # Valor por defecto

    merton = MertonModel(asset_value, debt, volatility, risk_free_rate, time_to_maturity)
    merton_results = merton.calculate()
    if merton_results['default_probability'] is not None:
        print(f"\nCalculated Merton Equity Value: ${merton_results['equity_value']:.2f}")
        print(f"Calculated Merton Default Probability: {merton_results['default_probability']:.2%}")
    else:
        print("Failed to calculate Merton model results.")
    
    evaluator = RiskEvaluator()
    print("\nRisk Evaluation:")
    print("Altman Z-Score Evaluation:", evaluator.evaluate_z_score(z_score))
    print("Merton Model Evaluation:", evaluator.evaluate_merton(merton_results['default_probability']))

if __name__ == "__main__":
    main()
