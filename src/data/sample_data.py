"""Sample data configuration for the MCS simulation.

Contains fiktive/anonymized input parameters for an example
offshore oil project, based on typical industry values.
"""
from dataclasses import dataclass


# === Example Project: "North Sea Offshore Field Alpha" ===
# All values are fictional and for illustration purposes only.

PROJECT_NAME = "North Sea Alpha (fiktiv)"

# CAPEX: Capital Expenditure (USD)
# Typical range for medium-sized offshore development
CAPEX_MIN = 500e6    # $500M — optimistic scenario
CAPEX_MODE = 750e6   # $750M — most likely
CAPEX_MAX = 1200e6   # $1.2B — pessimistic scenario

# OPEX: Operational Expenditure (USD/year)
# Annual operating costs over field lifetime
OPEX_MIN = 80e6     # $80M/year — efficient operations
OPEX_MODE = 120e6   # $120M/year — typical
OPEX_MAX = 200e6   # $200M/year — cost overruns

# Production Volume (barrels total over field life)
VOLUME_MIN = 50e6   # 50M bbl — P10 (low estimate)
VOLUME_MODE = 150e6  # 150M bbl — P50 (best estimate)
VOLUME_MAX = 300e6  # 300M bbl — P90 (high estimate)

# Oil Price (USD/barrel) — Lognormal parameters
OIL_PRICE_MEAN = 70  # $70/bbl expected
OIL_PRICE_SIGMA = 0.35  # Volatility parameter

# Simulation defaults
DEFAULT_ITERATIONS = 10000
DEFAULT_SEED = 42