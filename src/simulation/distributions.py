"""Distribution definitions for the MCS model."""
import numpy as np
from dataclasses import dataclass


@dataclass
class TriangularParams:
    """Triangular distribution parameters."""
    min: float
    mode: float
    max: float
    
    def sample(self, rng: np.random.Generator, size: int) -> np.ndarray:
        return rng.triangular(self.min, self.mode, self.max, size=size)
    
    def mean(self) -> float:
        return (self.min + self.mode + self.max) / 3
    
    def variance(self) -> float:
        a, m, b = self.min, self.mode, self.max
        return (a**2 + m**2 + b**2 - a*m - a*b - m*b) / 18


@dataclass
class LognormalParams:
    """Lognormal distribution parameters."""
    mean: float     # E[X] on original scale
    sigma: float     # σ of ln(X)
    
    @property
    def mu(self) -> float:
        return np.log(self.mean) - self.sigma**2 / 2
    
    def sample(self, rng: np.random.Generator, size: int) -> np.ndarray:
        return rng.lognormal(mean=self.mu, sigma=self.sigma, size=size)
    
    def mean_original(self) -> float:
        return np.exp(self.mu + self.sigma**2 / 2)
    
    def variance_original(self) -> float:
        return (np.exp(self.sigma**2) - 1) * np.exp(2 * self.mu + self.sigma**2)


# Default parameters for oil industry MCS
DEFAULT_CAPEX = TriangularParams(min=500e6, mode=750e6, max=1200e6)
DEFAULT_OPEX = TriangularParams(min=80e6, mode=120e6, max=200e6)
DEFAULT_VOLUME = TriangularParams(min=50e6, mode=150e6, max=300e6)
DEFAULT_OIL_PRICE = LognormalParams(mean=70, sigma=0.35)