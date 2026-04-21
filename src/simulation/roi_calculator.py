"""ROI calculation logic."""
import numpy as np


def compute_roi(capex: np.ndarray, opex: np.ndarray,
                volume: np.ndarray, oil_price: np.ndarray) -> np.ndarray:
    """
    Compute ROI for each simulation step.
    
    ROI = (OilPrice * Volume - CAPEX - OPEX) / CAPEX
    
    Parameters
    ----------
    capex : np.ndarray
        Capital expenditure values (investment costs)
    opex : np.ndarray
        Operational expenditure values (running costs)
    volume : np.ndarray
        Production volume in barrels
    oil_price : np.ndarray
        Oil price in $/barrel
    
    Returns
    -------
    np.ndarray
        ROI values for each simulation step
    """
    revenue = oil_price * volume
    total_cost = capex + opex
    profit = revenue - total_cost
    return profit / capex


def compute_roi_components(capex: np.ndarray, opex: np.ndarray,
                            volume: np.ndarray, oil_price: np.ndarray) -> dict:
    """
    Compute ROI with detailed component breakdown.
    
    Returns dict with revenue, costs, profit, roi, and component ratios.
    """
    revenue = oil_price * volume
    total_cost = capex + opex
    profit = revenue - total_cost
    roi = profit / capex
    
    return {
        "revenue": revenue,
        "total_cost": total_cost,
        "profit": profit,
        "roi": roi,
        "revenue_per_capex": revenue / capex,
        "opex_per_capex": opex / capex,
        "revenue_per_barrel": oil_price,
        "cost_per_barrel": total_cost / np.where(volume > 0, volume, 1),
    }