"""Sensitivity analysis visualization — Tornado diagram."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'simulation'))
from mcs_engine import SimulationConfig, sensitivity_analysis


def plot_tornado(sensitivity: dict, save_path: str = None):
    """
    Plot a Tornado diagram showing variance contribution of each input variable.
    
    Parameters
    ----------
    sensitivity : dict
        Output from sensitivity_analysis()
    save_path : str, optional
        Path to save the figure.
    """
    # Sort by contribution (ascending for horizontal bar chart)
    items = sorted(sensitivity.items(), key=lambda x: x[1])
    labels = [k.replace('_', ' ').title() for k, v in items]
    values = [v for k, v in items]
    
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12']
    bars = ax.barh(labels, values, color=colors[:len(labels)], edgecolor='white', height=0.6)
    
    # Add percentage labels
    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height() / 2,
                f'{val:.1%}', va='center', fontsize=12, fontweight='bold')
    
    ax.set_xlabel('Variance Contribution (%)', fontsize=12)
    ax.set_title('Sensitivitaetsanalyse: Varianzbeitrag der Input-Variablen', 
                 fontsize=14, fontweight='bold')
    ax.set_xlim(0, max(values) * 1.15)
    ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.savefig(save_path.replace('.png', '.pdf'), bbox_inches='tight')
        print(f"Tornado diagram saved to {save_path}")
        plt.close()
    else:
        plt.show()


if __name__ == '__main__':
    config = SimulationConfig(n_iterations=10000, random_seed=42)
    sens = sensitivity_analysis(config)
    
    print("Sensitivity results:")
    for var, contrib in sorted(sens.items(), key=lambda x: -x[1]):
        print(f"  {var:>15}: {contrib:.1%}")
    
    figures_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'docs', 'paper', 'figures')
    os.makedirs(figures_dir, exist_ok=True)
    
    plot_tornado(sens, save_path=os.path.join(figures_dir, 'sensitivity_tornado.png'))