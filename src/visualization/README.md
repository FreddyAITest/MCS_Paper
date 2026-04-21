# Visualization Module

This module generates charts and diagrams from the simulation results.

## Files

- `histogram.py` — Creates the ROI distribution histogram with key statistics
- `sensitivity.py` — Generates tornado diagrams for sensitivity analysis

## Quick Start

```bash
# After running the simulation:
python src/simulation/mcs_engine.py --iterations 10000 --sensitivity

# Generate visualization:
python src/visualization/histogram.py
python src/visualization/sensitivity.py
```