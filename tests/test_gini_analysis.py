"""
Tests for gini_analysis module.
"""

import numpy as np
import pytest
from src.simulation.gini_analysis import (
    gini_coefficient,
    gini_feature_importance,
    tree_gini_importance,
    SimulationConfig,
    run_gini_analysis,
)


class TestGiniCoefficient:
    """Tests for the Gini coefficient computation."""

    def test_perfect_equality(self):
        """All equal values → Gini = 0."""
        x = np.ones(1000) * 10.0
        g = gini_coefficient(x)
        assert g == pytest.approx(0.0, abs=1e-6)

    def test_maximal_inequality(self):
        """One value has everything, rest have zero → Gini near 1."""
        x = np.zeros(1000)
        x[0] = 1000.0
        g = gini_coefficient(x)
        assert g > 0.99  # (n-1)/n for discrete case

    def test_uniform_distribution(self):
        """Uniform distribution has a known Gini = (n-1) / (3n) ≈ 1/3 for large n."""
        rng = np.random.default_rng(42)
        x = rng.uniform(0, 1, 100000)
        g = gini_coefficient(x)
        # Theoretical Gini for U(0,1) = 1/3 ≈ 0.333
        assert g == pytest.approx(1/3, abs=0.02)

    def test_lognormal_higher_gini_than_triangular(self):
        """Lognormal should have higher Gini than Triangular with same mean."""
        rng = np.random.default_rng(42)
        n = 10000
        
        # Triangular
        tri = rng.triangular(80e6, 120e6, 200e6, size=n)
        # Lognormal with similar mean
        mu = np.log(120e6) - 0.35**2 / 2
        lognorm = rng.lognormal(mean=mu, sigma=0.35, size=n)
        
        g_tri = gini_coefficient(tri)
        g_log = gini_coefficient(lognorm)
        
        # Lognormal typically has higher Gini due to heavier right tail
        assert g_log > g_tri

    def test_negative_values_handled(self):
        """Negative values should be handled by shifting."""
        x = np.array([-5, -3, -1, 1, 3, 5])
        g = gini_coefficient(x)
        assert 0.0 <= g <= 1.0

    def test_empty_array(self):
        """Empty array returns 0."""
        g = gini_coefficient(np.array([]))
        assert g == 0.0

    def test_single_value(self):
        """Single value → Gini = 0."""
        g = gini_coefficient(np.array([42.0]))
        assert g == pytest.approx(0.0, abs=1e-6)

    def test_known_gini_two_values(self):
        """Two values: known Gini = |x1-x2| / (2*(x1+x2))."""
        x = np.array([10, 50])
        g = gini_coefficient(x)
        expected = 40 / (2 * 60)  # = 1/3
        assert g == pytest.approx(expected, abs=0.01)


class TestGiniFeatureImportance:
    """Tests for the conditional Gini feature importance."""

    def test_oil_price_most_important(self):
        """Oil price should be the most important feature."""
        rng = np.random.default_rng(42)
        n = 5000
        
        capex = rng.triangular(500e6, 750e6, 1200e6, size=n)
        opex = rng.triangular(80e6, 120e6, 200e6, size=n)
        volume = rng.triangular(50e6, 150e6, 300e6, size=n)
        oil_price = rng.lognormal(mean=4.19, sigma=0.35, size=n)
        roi = (oil_price * volume - capex - opex) / capex
        
        inputs = {"oil_price": oil_price, "volume": volume, "capex": capex, "opex": opex}
        imp = gini_feature_importance(inputs, roi, n_bins=20)
        
        # Oil price should dominate
        assert imp["oil_price"] > imp["capex"]
        assert imp["oil_price"] > imp["opex"]

    def test_importance_sums_to_one(self):
        """Feature importance should sum to ~1."""
        rng = np.random.default_rng(42)
        n = 5000
        
        capex = rng.triangular(500e6, 750e6, 1200e6, size=n)
        opex = rng.triangular(80e6, 120e6, 200e6, size=n)
        volume = rng.triangular(50e6, 150e6, 300e6, size=n)
        oil_price = rng.lognormal(mean=4.19, sigma=0.35, size=n)
        roi = (oil_price * volume - capex - opex) / capex
        
        inputs = {"oil_price": oil_price, "volume": volume, "capex": capex, "opex": opex}
        imp = gini_feature_importance(inputs, roi, n_bins=20)
        
        total = sum(imp.values())
        assert total == pytest.approx(1.0, abs=0.05)


class TestTreeGiniImportance:
    """Tests for the tree-based Gini importance."""

    def test_oil_price_dominates(self):
        """Oil price should be the most important feature in tree model."""
        rng = np.random.default_rng(42)
        n = 3000
        
        capex = rng.triangular(500e6, 750e6, 1200e6, size=n)
        opex = rng.triangular(80e6, 120e6, 200e6, size=n)
        volume = rng.triangular(50e6, 150e6, 300e6, size=n)
        oil_price = rng.lognormal(mean=4.19, sigma=0.35, size=n)
        roi = (oil_price * volume - capex - opex) / capex
        
        inputs = {"oil_price": oil_price, "volume": volume, "capex": capex, "opex": opex}
        imp = tree_gini_importance(inputs, roi, max_depth=4, n_trees=50, random_seed=42)
        
        assert imp["oil_price"] > imp["opex"]
        assert imp["oil_price"] > 0.2  # Should be significant

    def test_importance_sum(self):
        """Tree importance values should sum to ~1."""
        rng = np.random.default_rng(42)
        n = 2000
        
        capex = rng.triangular(500e6, 750e6, 1200e6, size=n)
        opex = rng.triangular(80e6, 120e6, 200e6, size=n)
        volume = rng.triangular(50e6, 150e6, 300e6, size=n)
        oil_price = rng.lognormal(mean=4.19, sigma=0.35, size=n)
        roi = (oil_price * volume - capex - opex) / capex
        
        inputs = {"oil_price": oil_price, "volume": volume, "capex": capex, "opex": opex}
        imp = tree_gini_importance(inputs, roi, max_depth=4, n_trees=50, random_seed=42)
        
        total = sum(imp.values())
        assert total == pytest.approx(1.0, abs=0.01)


class TestRunGiniAnalysis:
    """Integration tests for the full analysis pipeline."""

    def test_full_analysis_runs(self):
        """Full analysis should run without error and return expected keys."""
        config = SimulationConfig(n_iterations=1000, random_seed=42)
        results = run_gini_analysis(config, verbose=False)
        
        assert "input_gini" in results
        assert "roi_gini" in results
        assert "feature_importance_conditional" in results
        assert "feature_importance_tree" in results
        assert "sensitivity_variance" in results
        
        # All Gini values should be between 0 and 1
        for name, g in results["input_gini"].items():
            assert 0 <= g <= 1, f"{name} Gini = {g} out of range"
        
        assert 0 <= results["roi_gini"] <= 1

    def test_oil_price_highest_importance(self):
        """Oil price should have highest importance across all methods."""
        config = SimulationConfig(n_iterations=1000, random_seed=42)
        results = run_gini_analysis(config, verbose=False)
        
        cond = results["feature_importance_conditional"]
        assert cond["oil_price"] == max(cond.values())


if __name__ == "__main__":
    pytest.main([__file__, "-v"])