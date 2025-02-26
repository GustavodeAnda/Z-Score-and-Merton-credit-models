"""
Package for Credit Risk Models, including Altman Z-Score and Merton Model implementations.

Modules included:
    - data_loader: For downloading financial data using yfinance.
    - altman_z_score: For calculating the Altman Z-Score.
    - merton_model: For estimating default probability using the Merton model.
    - risk_evaluator: For evaluating risk based on the results of the models.
    - utils: Utility functions for calculations.
"""

__version__ = "0.1.0"

from .data_loader import DataLoader
from .altman_z_score import AltmanZScore
from .merton_model import MertonModel
from .risk_evaluator import RiskEvaluator
from .utils import calculate_ratios, black_scholes

