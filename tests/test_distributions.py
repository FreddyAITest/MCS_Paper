"""Tests for distribution definitions."""
import numpy as np
import pytest
from src.simulation.distributions import TriangularParams, LognormalParams


class TestTriangularParams:
    def test_mean(self):
        """Mean of Tri(a, m, b) should be (a + m + b) / 3."""
        tp = TriangularParams(min=1, mode=2, max=3)
        assert abs(tp.mean() - 2.0) < 1e-10

    def test_variance(self):
        """Variance of Tri(a, m, b) should be (a^2 + m^2 + b^2 - am - ab - mb) / 18."""
        tp = TriangularParams(min=1, mode=2, max=3)
        expected_var = (1 + 4 + 9 - 2 - 3 - 6) / 18
        assert abs(tp.variance() - expected_var) < 1e-10

    def test_sample_shape(self):
        """Sample should return correct number of values."""
        tp = TriangularParams(min=100, mode=200, max=300)
        rng = np.random.default_rng(42)
        samples = tp.sample(rng, size=10000)
        assert samples.shape == (10000,)

    def test_sample_bounds(self):
        """All samples should be within [min, max]."""
        tp = TriangularParams(min=100, mode=200, max=300)
        rng = np.random.default_rng(42)
        samples = tp.sample(rng, size=100000)
        assert np.all(samples >= 100)
        assert np.all(samples <= 300)

    def test_sample_converges_to_mean(self):
        """Sample mean should converge to theoretical mean."""
        tp = TriangularParams(min=500e6, mode=750e6, max=1200e6)
        rng = np.random.default_rng(42)
        samples = tp.sample(rng, size=100000)
        assert abs(np.mean(samples) - tp.mean()) / tp.mean() < 0.01


class TestLognormalParams:
    def test_mu_property(self):
        """mu should equal ln(mean) - sigma^2 / 2."""
        lp = LognormalParams(mean=70, sigma=0.35)
        expected_mu = np.log(70) - 0.35**2 / 2
        assert abs(lp.mu - expected_mu) < 1e-10

    def test_sample_shape(self):
        """Sample should return correct number of values."""
        lp = LognormalParams(mean=70, sigma=0.35)
        rng = np.random.default_rng(42)
        samples = lp.sample(rng, size=10000)
        assert samples.shape == (10000,)

    def test_sample_positive(self):
        """All lognormal samples should be positive."""
        lp = LognormalParams(mean=70, sigma=0.35)
        rng = np.random.default_rng(42)
        samples = lp.sample(rng, size=100000)
        assert np.all(samples > 0)

    def test_sample_converges_to_mean(self):
        """Sample mean should converge to specified mean."""
        lp = LognormalParams(mean=70, sigma=0.35)
        rng = np.random.default_rng(42)
        samples = lp.sample(rng, size=100000)
        # Allow 5% tolerance due to lognormal variance
        assert abs(np.mean(samples) - lp.mean_original()) / lp.mean_original() < 0.05