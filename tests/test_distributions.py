"""Tests for distribution definitions."""
import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'simulation'))

from distributions import TriangularParams, LognormalParams, DEFAULT_CAPEX, DEFAULT_OPEX, DEFAULT_VOLUME, DEFAULT_OIL_PRICE


class TestTriangularParams:
    """Test suite for TriangularParams."""

    def test_mean_calculation(self):
        p = TriangularParams(min=100, mode=200, max=400)
        assert p.mean() == pytest.approx(233.333, rel=1e-3)

    def test_variance_calculation(self):
        p = TriangularParams(min=100, mode=200, max=400)
        var = p.variance()
        assert var > 0

    def test_sample_shape(self):
        p = TriangularParams(min=100, mode=200, max=400)
        rng = np.random.default_rng(42)
        samples = p.sample(rng, size=1000)
        assert samples.shape == (1000,)

    def test_sample_within_bounds(self):
        p = TriangularParams(min=100, mode=200, max=400)
        rng = np.random.default_rng(42)
        samples = p.sample(rng, size=10000)
        assert np.all(samples >= 100)
        assert np.all(samples <= 400)

    def test_sample_mode_concentration(self):
        p = TriangularParams(min=100, mode=200, max=400)
        rng = np.random.default_rng(42)
        samples = p.sample(rng, size=100000)
        # Mode should be near the peak of the histogram
        hist, bin_edges = np.histogram(samples, bins=50)
        peak_bin = np.argmax(hist)
        peak_center = (bin_edges[peak_bin] + bin_edges[peak_bin + 1]) / 2
        assert abs(peak_center - 200) < 30

    def test_default_capex(self):
        assert DEFAULT_CAPEX.min == 500e6
        assert DEFAULT_CAPEX.mode == 750e6
        assert DEFAULT_CAPEX.max == 1200e6

    def test_default_opex(self):
        assert DEFAULT_OPEX.min == 80e6
        assert DEFAULT_OPEX.mode == 120e6
        assert DEFAULT_OPEX.max == 200e6

    def test_default_volume(self):
        assert DEFAULT_VOLUME.min == 50e6
        assert DEFAULT_VOLUME.mode == 150e6
        assert DEFAULT_VOLUME.max == 300e6


class TestLognormalParams:
    """Test suite for LognormalParams."""

    def test_mu_calculation(self):
        p = LognormalParams(mean=70, sigma=0.35)
        expected_mu = np.log(70) - 0.35**2 / 2
        assert p.mu == pytest.approx(expected_mu, rel=1e-6)

    def test_mean_original(self):
        p = LognormalParams(mean=70, sigma=0.35)
        # E[X] = exp(mu + sigma^2/2) should be close to 70
        assert p.mean_original() == pytest.approx(70, rel=1e-6)

    def test_variance_positive(self):
        p = LognormalParams(mean=70, sigma=0.35)
        assert p.variance_original() > 0

    def test_sample_positive(self):
        p = LognormalParams(mean=70, sigma=0.35)
        rng = np.random.default_rng(42)
        samples = p.sample(rng, size=10000)
        assert np.all(samples > 0)

    def test_sample_shape(self):
        p = LognormalParams(mean=70, sigma=0.35)
        rng = np.random.default_rng(42)
        samples = p.sample(rng, size=1000)
        assert samples.shape == (1000,)

    def test_default_oil_price(self):
        assert DEFAULT_OIL_PRICE.mean == 70
        assert DEFAULT_OIL_PRICE.sigma == 0.35