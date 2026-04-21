"""Tests for ROI calculator."""
import numpy as np
import pytest
from src.simulation.roi_calculator import compute_roi, compute_roi_components


class TestComputeROI:
    def test_simple_case(self):
        """Basic ROI calculation with known values."""
        # ROI = (70 * 150M - 750M - 120M) / 750M = (10500M - 870M) / 750M = 12.84
        capex = np.array([750e6])
        opex = np.array([120e6])
        volume = np.array([150e6])
        oil_price = np.array([70])
        
        roi = compute_roi(capex, opex, volume, oil_price)
        expected = (70 * 150e6 - 750e6 - 120e6) / 750e6
        assert abs(roi[0] - expected) < 1e-6

    def test_zero_profit(self):
        """ROI should be 0 when revenue equals costs."""
        # revenue = 70 * 10 = 700, costs = 400 + 300 = 700 => ROI = 0
        capex = np.array([400])
        opex = np.array([300])
        volume = np.array([10])
        oil_price = np.array([70])
        
        roi = compute_roi(capex, opex, volume, oil_price)
        assert abs(roi[0]) < 1e-10

    def test_negative_roi(self):
        """ROI should be negative when costs exceed revenue."""
        capex = np.array([1000])
        opex = np.array([500])
        volume = np.array([10])
        oil_price = np.array([10])  # very low price
        
        roi = compute_roi(capex, opex, volume, oil_price)
        assert roi[0] < 0

    def test_array_input(self):
        """Should work with arrays of different values."""
        n = 1000
        capex = np.full(n, 750e6)
        opex = np.full(n, 120e6)
        volume = np.full(n, 150e6)
        oil_price = np.full(n, 70)
        
        roi = compute_roi(capex, opex, volume, oil_price)
        assert roi.shape == (n,)
        assert np.all(roi > 0)  # all should be positive with these inputs


class TestComputeROIComponents:
    def test_components_return_dict(self):
        """Should return a dict with all expected keys."""
        capex = np.array([750e6])
        opex = np.array([120e6])
        volume = np.array([150e6])
        oil_price = np.array([70])
        
        result = compute_roi_components(capex, opex, volume, oil_price)
        assert 'revenue' in result
        assert 'total_cost' in result
        assert 'profit' in result
        assert 'roi' in result
        assert 'revenue_per_capex' in result
        assert 'opex_per_capex' in result