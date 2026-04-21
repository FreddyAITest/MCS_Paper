"""Generate ROI histogram from simulation results."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
import os

# Add parent directory for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'simulation'))
from mcs_engine import SimulationConfig, run_simulation


def plot_roi_histogram(result: dict, save_path: str = None):
    """
    Plot the ROI distribution as a histogram with key statistics.
    
    Parameters
    ----------
    result : dict
        Output from run_simulation()
    save_path : str, optional
        Path to save the figure. If None, displays interactively.
    """
    roi = result['roi']
    stats = result['statistics']
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Histogram
    n, bins, patches = ax.hist(roi, bins=80, density=True, alpha=0.7, 
                                 color='steelblue', edgecolor='white', linewidth=0.5)
    
    # Color negative ROI bins red
    for patch, left_edge in zip(patches, bins[:-1]):
        if left_edge < 0:
            patch.set_facecolor('#e74c3c')
            patch.set_alpha(0.7)
    
    # Vertical lines for key statistics
    ax.axvline(stats['mean_roi'], color='#2c3e50', linestyle='-', linewidth=2, 
               label=f'Mean: {stats["mean_roi"]:.1%}')
    ax.axvline(0, color='black', linestyle='--', linewidth=1.5, 
               label=f'Break-even')
    ax.axvline(stats['var_5pct'], color='#e67e22', linestyle=':', linewidth=2, 
               label=f'VaR 5%: {stats["var_5pct"]:.1%}')
    ax.axvline(stats['median_roi'], color='#27ae60', linestyle='-.', linewidth=1.5, 
               label=f'Median (P50): {stats["median_roi"]:.1%}')
    
    # Styling
    ax.set_xlabel('Return on Investment (ROI)', fontsize=13)
    ax.set_ylabel('Probability Density', fontsize=13)
    ax.set_title('Monte-Carlo-Simulation: ROI-Verteilung\n'
                 f'n={len(roi):,} Iterationen | P(ROI<0)={stats["prob_loss"]:.1%}', 
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=11, loc='upper right')
    ax.grid(axis='y', alpha=0.3)
    
    # Statistics box
    stats_text = (f'Mean: {stats["mean_roi"]:.1%}\n'
                  f'Median: {stats["median_roi"]:.1%}\n'
                  f'Std Dev: {stats["std_roi"]:.1%}\n'
                  f'VaR 5%: {stats["var_5pct"]:.1%}\n'
                  f'CVaR 5%: {stats["cvar_5pct"]:.1%}\n'
                  f'P(Loss): {stats["prob_loss"]:.1%}')
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    ax.text(0.02, 0.97, stats_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.savefig(save_path.replace('.png', '.pdf'), bbox_inches='tight')
        print(f"Histogram saved to {save_path}")
        plt.close()
    else:
        plt.show()


if __name__ == '__main__':
    config = SimulationConfig(n_iterations=10000, random_seed=42)
    result = run_simulation(config)
    
    figures_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'docs', 'paper', 'figures')
    os.makedirs(figures_dir, exist_ok=True)
    
    plot_roi_histogram(result, save_path=os.path.join(figures_dir, 'roi_distribution.png'))