"""Tests for the MCS engine."""
import numpy as np
import pytest
from src.simulation.mcs_engine import SimulationConfig, run_simulation, sensitivity_analysis


class TestRunSimulation:
    def test_returns_dict_with_expected_keys(self):
        result = run_simulation(SimulationConfig(n_iterations=100, random_seed=42))
        assert 'roi' in result
        assert 'capex' in result
        assert 'opex' in result
        assert 'volume' in result
        assert 'oil_price' in result
        assert 'statistics' in result

    def test_roi_array_length(self):
        """ROI array should have n_iterations elements."""
        n = 500
        result = run_simulation(SimulationConfig(n_iterations=n, random_seed=42))
        assert len(result['roi']) == n

    def test_statistics_keys(self):
        """Statistics dict should contain all expected keys."""
        result = run_simulation(SimulationConfig(n_iterations=100, random_seed=42))
        stats = result['statistics']
        expected_keys = ['mean_roi', 'median_roi', 'std_roi', 'var_5pct', 
                        'var_1pct', 'cvar_5pct', 'prob_loss', 'min_roi', 'max_roi', 'rarr']
        for key in expected_keys:
            assert key in stats, f"Missing key: {key}"

    def test_reproducibility(self):
        """Same seed should produce same results."""
        r1 = run_simulation(SimulationConfig(n_iterations=100, random_seed=42))
        r2 = run_simulation(SimulationConfig(n_iterations=100, random_seed=42))
        assert np.array_equal(r1['roi'], r2['roi'])

    def test_different_seeds_differ(self):
        """Different seeds should produce different results."""
        r1 = run_simulation(SimulationConfig(n_iterations=1000, random_seed=42))
        r2 = run_simulation(SimulationConfig(n_iterations=1000, random_seed=99))
        assert not np.array_equal(r1['roi'], r2['roi'])

    def test_prob_loss_between_0_and_1(self):
        """Probability of loss should be between 0 and 1."""
        result = run_simulation(SimulationConfig(n_iterations=10000, random_seed=42))
        prob = result['statistics']['prob_loss']
        assert 0 <= prob <= 1

    def test_large_simulation_converges(self):
        """10000 iterations should produce stable statistics."""
        r1 = run_simulation(SimulationConfig(n_iterations=10000, random_seed=42))
        r2 = run_simulation(SimulationConfig(n_iterations=10000, random_seed=43))
        # Means should be within 10% of each other
        assert abs(r1['statistics']['mean_roi'] - r2['statistics']['mean_roi']) / \
               abs(r1['statistics']['mean_roi']) < 0.1


class TestSensitivityAnalysis:
    def test_returns_dict(self):
        sens = sensitivity_analysis(SimulationConfig(n_iterations=100, random_seed=42),
                                     n_iterations=100)
        assert isinstance(sens, dict)

    def test_all_variables_present(self):
        sens = sensitivity_analysis(SimulationConfig(n_iterations=100, random_seed=42),
                                     n_iterations=100)
        assert 'capex' in sens
        assert 'opex' in sens
        assert 'volume' in sens
        assert 'oil_price' in sens

    def test_contributions_positive(self):
        sens = sensitivity_analysis(SimulationConfig(n_iterations=1000, random_seed=42),
                                     n_iterations=1000)
        for var, contrib in sens.items():
            assert contrib >= 0, f"{var} has negative contribution: {contrib}"