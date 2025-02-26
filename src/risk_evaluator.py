"""
risk_evaluator.py

This module contains the RiskEvaluator class, which evaluates the risk based on the results 
obtained from the Altman Z-Score and the Merton Model. The evaluations are made separately for each model.

Evaluations:
    Altman Z-Score:
        - Z < 1.8: High risk of bankruptcy.
        - 1.8 <= Z < 3.0: Medium risk.
        - Z >= 3.0: Low risk of bankruptcy.
        
    Merton Model (Default Probability):
        - Default Probability > 10%: High default risk.
        - Default Probability < 5%: Low default risk.
        - Otherwise: Moderate default risk.
"""

class RiskEvaluator:
    def __init__(self):
        """
        Initializes the RiskEvaluator.
        """
        pass

    def evaluate_z_score(self, z_score: float) -> str:
        """
        Evaluates the Altman Z-Score.

        :param z_score: The calculated Altman Z-Score.
        :return: A string describing the risk level based on the Z-Score.
        """
        if z_score < 1.8:
            return "High bankruptcy risk"
        elif z_score >= 3.0:
            return "Low bankruptcy risk"
        else:
            return "Medium bankruptcy risk"

    def evaluate_merton(self, default_probability: float) -> str:
        """
        Evaluates the default probability from the Merton Model.

        :param default_probability: The calculated default probability (as a decimal).
        :return: A string describing the default risk level.
        """
        if default_probability > 0.10:
            return "High default risk"
        elif default_probability < 0.05:
            return "Low default risk"
        else:
            return "Moderate default risk"

    def display_results(self, z_score: float, default_probability: float) -> None:
        """
        Displays the evaluation results for both the Altman Z-Score and Merton Model.

        :param z_score: The calculated Altman Z-Score.
        :param default_probability: The calculated default probability from the Merton Model.
        """
        z_evaluation = self.evaluate_z_score(z_score)
        m_evaluation = self.evaluate_merton(default_probability)
        
        print("\n=== Risk Evaluations ===")
        print(f"Altman Z-Score: {z_score:.2f} -> {z_evaluation}")
        print(f"Merton Default Probability: {default_probability:.2%} -> {m_evaluation}")

if __name__ == "__main__":
    # Example usage:
    # These values are sample values for demonstration purposes.
    sample_z_score = 2.5
    sample_default_probability = 0.07  # 7%
    
    evaluator = RiskEvaluator()
    evaluator.display_results(sample_z_score, sample_default_probability)
