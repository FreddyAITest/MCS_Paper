"""Tests for the ROI calculator."""
import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'simulation'))

from roi_calculator import compute_roi, compute_roi_components


class TestComputeROI:
    """Test suite for compute_roi."""

    def test_simple_break_even(self):
        """When revenue equals total cost, ROI should be zero."""
        capex = np.array([100.0])
        opex = np.array([20.0])
        volume = np.array([10.0])
        oil_price = np.array([12.0])  # revenue = 12 * 10 = 120 = capex + opex
        roi = compute_roi(capex, opex, volume, oil_price)
        assert roi[0] == pytest.approx(0.0)

    def test_positive_roi(self):
        capex = np.array([100.0])
        opex = np.array([20.0])
        volume = np.array([10.0])
        oil_price = np.array([20.0])  # revenue = 200, cost = 120, profit = 80
        roi = compute_roi(capex, opex, volume, oil_price)
        assert roi[0] == pytest.approx(0.8)

    def test_negative_roi(self):
        capex = np.array([100.0])
        opex = np.array([20.0])
        volume = np.array([10.0])
        oil_price = np.array([5.0])  # revenue = 50, cost = 120, profit = -70
        roi = compute_roi(capex, opex, volume, oil_price)
        assert roi[0] == pytest.approx(-0.7)

    def test_array_computation(self):
        n = 5
        capex = np.full(n, 100.0)
        opex = np.full(n, 20.0)
        volume = np.full(n, 10.0)
        oil_price = np.full(n, 15.0)
        roi = compute_roi(capex, opex, volume, oil_price)
        assert len(roi) == n
        assert np.allclose(roi, 0.3)

    def test_formula_equivalence(self):
        """verify ROI = (P*V - CAPEX - OPEX) / CAPEX"""
        capex = np.array([500e6, 750e6, 1000e6])
        opex = np.array([100e6, 120e6, 150e6])
        volume = np.array([100e6, 150e6, 200e6])
        oil_price = np.array([70.0, 80.0, 90.0])
        roi = compute_roi(capex, opex, volume, oil_price)
        expected = (oil_price * volume - capex - opex) / capex
        assert np.allclose(roi, expected)


class TestComputeROIComponents:
    """Test suite for compute_roi_components."""

    def test_component_breakdown(self):
        capex = np.array([100.0])
        opex = np.array([20.0])
        volume = np.array([10.0])
        oil_price = np.array([15.0])
        result = compute_roi_components(capex, opex, volume, oil_price)
        assert "revenue" in result
        assert "total_cost" in result
        assert "profit" in result
        assert "roi" in result
        assert "revenue_per_capex" in result
        assert "opex_per_capex" in result

    def test_revenue_calculation(self):
        capex = np.array([100.0])
        opex = np.array([20.0])
        volume = np.array([10.0])
        oil_price = np.array([15.0])
        result = compute_roi_components(capex, opex, volume, oil_price)
        assert result["revenue"][0] == pytest.approx(150.0)
        assert result["total_cost"][0] == pytest.approx(120.0)