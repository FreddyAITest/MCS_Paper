"""
MCS_Paper — Monte-Carlo-Simulation für ROI-Bewertung in der Ölindustrie

Core simulation engine.
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TriangularParams:
    """Parameters for a Triangular distribution."""
    min: float      # a — worst case
    mode: float     # m — most likely
    max: float      # b — best case


@dataclass 
class LognormalParams:
    """Parameters for a Lognormal distribution."""
    mean: float     # E[X] on original scale
    sigma: float     # σ of log(X)
    
    @property
    def mu(self) -> float:
        """μ parameter of log(X) distribution."""
        return np.log(self.mean) - self.sigma**2 / 2


@dataclass
class SimulationConfig:
    """Configuration for the Monte-Carlo simulation."""
    n_iterations: int = 10000
    random_seed: Optional[int] = 42
    capex: TriangularParams = field(default_factory=lambda: TriangularParams(min=500e6, mode=750e6, max=1200e6))
    opex: TriangularParams = field(default_factory=lambda: TriangularParams(min=80e6, mode=120e6, max=200e6))
    volume: TriangularParams = field(default_factory=lambda: TriangularParams(min=50e6, mode=150e6, max=300e6))
    oil_price: LognormalParams = field(default_factory=lambda: LognormalParams(mean=70, sigma=0.35))


def sample_triangular(params: TriangularParams, rng: np.random.Generator, size: int) -> np.ndarray:
    """Sample from a Triangular distribution."""
    return rng.triangular(params.min, params.mode, params.max, size=size)


def sample_lognormal(params: LognormalParams, rng: np.random.Generator, size: int) -> np.ndarray:
    """Sample from a Lognormal distribution."""
    return rng.lognormal(mean=params.mu, sigma=params.sigma, size=size)


def compute_roi(capex: np.ndarray, opex: np.ndarray, 
                volume: np.ndarray, oil_price: np.ndarray) -> np.ndarray:
    """
    Compute ROI for each simulation step.
    
    ROI = (OilPrice × Volume - CAPEX - OPEX) / CAPEX
    """
    revenue = oil_price * volume
    total_cost = capex + opex
    profit = revenue - total_cost
    roi = profit / capex
    return roi


def run_simulation(config: SimulationConfig) -> dict:
    """
    Run the full Monte-Carlo simulation.
    
    Returns dict with:
        - roi: array of ROI values
        - capex, opex, volume, oil_price: sampled input arrays
        - statistics: dict of summary statistics
    """
    rng = np.random.default_rng(config.random_seed)
    n = config.n_iterations
    
    # Sample input variables
    capex = sample_triangular(config.capex, rng, n)
    opex = sample_triangular(config.opex, rng, n)
    volume = sample_triangular(config.volume, rng, n)
    oil_price = sample_lognormal(config.oil_price, rng, n)
    
    # Compute ROI
    roi = compute_roi(capex, opex, volume, oil_price)
    
    # Statistics
    stats = {
        "mean_roi": float(np.mean(roi)),
        "median_roi": float(np.median(roi)),
        "std_roi": float(np.std(roi)),
        "var_5pct": float(np.percentile(roi, 5)),
        "var_1pct": float(np.percentile(roi, 1)),
        "cvar_5pct": float(np.mean(roi[roi <= np.percentile(roi, 5)])),
        "prob_loss": float(np.mean(roi < 0)),
        "min_roi": float(np.min(roi)),
        "max_roi": float(np.max(roi)),
        "rarr": float(np.mean(roi) / np.std(roi)) if np.std(roi) > 0 else float('inf'),
    }
    
    return {
        "roi": roi,
        "capex": capex,
        "opex": opex,
        "volume": volume,
        "oil_price": oil_price,
        "statistics": stats,
    }


def _narrow_tri(params: TriangularParams, width_pct: float = 0.001) -> TriangularParams:
    """Create a very narrow triangular distribution centered at the mode."""
    mode = params.mode
    delta = mode * width_pct
    return TriangularParams(min=mode - delta, mode=mode, max=mode + delta)


def sensitivity_analysis(config: SimulationConfig, n_iterations: int = 10000) -> dict:
    """
    Simple one-at-a-time sensitivity analysis.
    Measures variance contribution of each variable by freezing it
    (using a very narrow distribution) and comparing total variance.
    """
    # First: full simulation (baseline)
    baseline = run_simulation(config)
    baseline_var = np.var(baseline["roi"])
    
    if baseline_var == 0:
        return {"capex": 0, "opex": 0, "volume": 0, "oil_price": 0}
    
    results = {}
    
    # CAPEX frozen
    cfg = SimulationConfig(
        n_iterations=n_iterations,
        random_seed=config.random_seed,
        capex=_narrow_tri(config.capex),
        opex=config.opex,
        volume=config.volume,
        oil_price=config.oil_price,
    )
    sim = run_simulation(cfg)
    results["capex"] = max(0, (baseline_var - np.var(sim["roi"])) / baseline_var)
    
    # OPEX frozen
    cfg = SimulationConfig(
        n_iterations=n_iterations,
        random_seed=config.random_seed,
        capex=config.capex,
        opex=_narrow_tri(config.opex),
        volume=config.volume,
        oil_price=config.oil_price,
    )
    sim = run_simulation(cfg)
    results["opex"] = max(0, (baseline_var - np.var(sim["roi"])) / baseline_var)
    
    # Volume frozen
    cfg = SimulationConfig(
        n_iterations=n_iterations,
        random_seed=config.random_seed,
        capex=config.capex,
        opex=config.opex,
        volume=_narrow_tri(config.volume),
        oil_price=config.oil_price,
    )
    sim = run_simulation(cfg)
    results["volume"] = max(0, (baseline_var - np.var(sim["roi"])) / baseline_var)
    
    # Oil price frozen
    cfg = SimulationConfig(
        n_iterations=n_iterations,
        random_seed=config.random_seed,
        capex=config.capex,
        opex=config.opex,
        volume=config.volume,
        oil_price=LognormalParams(mean=config.oil_price.mean, sigma=0.001),
    )
    sim = run_simulation(cfg)
    results["oil_price"] = max(0, (baseline_var - np.var(sim["roi"])) / baseline_var)
    
    return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="MCS ROI Simulation")
    parser.add_argument("--iterations", type=int, default=10000, help="Number of iterations")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--sensitivity", action="store_true", help="Run sensitivity analysis")
    args = parser.parse_args()
    
    config = SimulationConfig(
        n_iterations=args.iterations,
        random_seed=args.seed,
    )
    
    result = run_simulation(config)
    
    print("=" * 60)
    print("Monte-Carlo-Simulation: ROI in der Ölindustrie")
    print("=" * 60)
    print(f"Iterationen: {args.iterations:,}")
    print()
    print("ROI-Statistiken:")
    print(f"  Mean ROI:         {result['statistics']['mean_roi']:.2%}")
    print(f"  Median ROI:       {result['statistics']['median_roi']:.2%}")
    print(f"  Std Dev:          {result['statistics']['std_roi']:.2%}")
    print(f"  VaR (5%):         {result['statistics']['var_5pct']:.2%}")
    print(f"  CVaR (5%):        {result['statistics']['cvar_5pct']:.2%}")
    print(f"  P(Loss):          {result['statistics']['prob_loss']:.2%}")
    print(f"  Min ROI:          {result['statistics']['min_roi']:.2%}")
    print(f"  Max ROI:          {result['statistics']['max_roi']:.2%}")
    print(f"  RARR:             {result['statistics']['rarr']:.3f}")
    
    if args.sensitivity:
        sens = sensitivity_analysis(config)
        print()
        print("Sensitivitätsanalyse (Varianzbeitrag):")
        for var, contrib in sorted(sens.items(), key=lambda x: -x[1]):
            print(f"  {var:>15}: {contrib:.1%}")
    
    print()
    print("=" * 60)