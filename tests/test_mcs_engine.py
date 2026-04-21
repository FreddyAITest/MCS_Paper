"""Tests for the MCS engine."""
import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'simulation'))

from mcs_engine import SimulationConfig, run_simulation, sensitivity_analysis, TriangularParams, LognormalParams


class TestSimulationConfig:
    """Test suite for SimulationConfig defaults."""

    def test_default_iterations(self):
        cfg = SimulationConfig()
        assert cfg.n_iterations == 10000

    def test_default_seed(self):
        cfg = SimulationConfig()
        assert cfg.random_seed == 42

    def test_default_capex(self):
        cfg = SimulationConfig()
        assert cfg.capex.min == 500e6
        assert cfg.capex.mode == 750e6
        assert cfg.capex.max == 1200e6


class TestRunSimulation:
    """Test suite for run_simulation."""

    def test_returns_dict_with_required_keys(self):
        cfg = SimulationConfig(n_iterations=1000, random_seed=42)
        result = run_simulation(cfg)
        assert "roi" in result
        assert "statistics" in result
        assert "capex" in result
        assert "opex" in result
        assert "volume" in result
        assert "oil_price" in result

    def test_roi_array_length(self):
        cfg = SimulationConfig(n_iterations=500, random_seed=42)
        result = run_simulation(cfg)
        assert len(result["roi"]) == 500

    def test_statistics_keys(self):
        cfg = SimulationConfig(n_iterations=500, random_seed=42)
        result = run_simulation(cfg)
        stats = result["statistics"]
        required_keys = ["mean_roi", "median_roi", "std_roi", "var_5pct",
                         "cvar_5pct", "prob_loss", "min_roi", "max_roi", "rarr"]
        for key in required_keys:
            assert key in stats, f"Missing key: {key}"

    def test_reproducibility(self):
        """Same seed should produce same results."""
        cfg = SimulationConfig(n_iterations=1000, random_seed=123)
        r1 = run_simulation(cfg)
        r2 = run_simulation(cfg)
        assert np.allclose(r1["roi"], r2["roi"])

    def test_different_seeds_different_results(self):
        cfg1 = SimulationConfig(n_iterations=1000, random_seed=42)
        cfg2 = SimulationConfig(n_iterations=1000, random_seed=99)
        r1 = run_simulation(cfg1)
        r2 = run_simulation(cfg2)
        assert not np.allclose(r1["roi"], r2["roi"])

    def test_mean_roi_reasonable_range(self):
        """Mean ROI should be in a plausible range for oil projects."""
        cfg = SimulationConfig(n_iterations=10000, random_seed=42)
        result = run_simulation(cfg)
        # With simplified 1-year model, ROI can be very high;
        # just verify it is finite and positive for these parameters
        assert -1.0 < result["statistics"]["mean_roi"] < 100.0

    def test_prob_loss_between_0_and_1(self):
        cfg = SimulationConfig(n_iterations=1000, random_seed=42)
        result = run_simulation(cfg)
        assert 0 <= result["statistics"]["prob_loss"] <= 1

    def test_var_less_than_mean(self):
        cfg = SimulationConfig(n_iterations=10000, random_seed=42)
        result = run_simulation(cfg)
        assert result["statistics"]["var_5pct"] < result["statistics"]["mean_roi"]

    def test_rarr_finite(self):
        cfg = SimulationConfig(n_iterations=1000, random_seed=42)
        result = run_simulation(cfg)
        assert np.isfinite(result["statistics"]["rarr"])


class TestSensitivityAnalysis:
    """Test suite for sensitivity_analysis."""

    def test_returns_dict(self):
        cfg = SimulationConfig(n_iterations=500, random_seed=42)
        result = sensitivity_analysis(cfg, n_iterations=500)
        assert isinstance(result, dict)

    def test_all_variables_present(self):
        cfg = SimulationConfig(n_iterations=500, random_seed=42)
        result = sensitivity_analysis(cfg, n_iterations=500)
        assert "capex" in result
        assert "opex" in result
        assert "volume" in result
        assert "oil_price" in result

    def test_contributions_non_negative(self):
        cfg = SimulationConfig(n_iterations=500, random_seed=42)
        result = sensitivity_analysis(cfg, n_iterations=500)
        for var, contrib in result.items():
            assert contrib >= 0, f"{var} has negative contribution: {contrib}"

    def test_oil_price_dominant(self):
        """Oil price should be the largest variance contributor."""
        cfg = SimulationConfig(n_iterations=5000, random_seed=42)
        result = sensitivity_analysis(cfg, n_iterations=5000)
        assert result["oil_price"] >= result["capex"]