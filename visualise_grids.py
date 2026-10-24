import numpy as np
import matplotlib.pyplot as plt
from ising_sim import Ising

def capture_state(temperature, grid_size=16):
    """Runs a targeted simulation at a single temperature to extract the final grid."""
    # Initialize for exactly 1 temperature point
    model = Ising(grid_size, nPoints=1, eqSteps=1000, mcSteps=1000)
    
    # Setup the C-compatible arrays
    spins = np.zeros((grid_size + 2, grid_size + 2), dtype=np.int32)
    E = np.zeros(1, dtype=np.float64)
    M = np.zeros(1, dtype=np.float64)
    C = np.zeros(1, dtype=np.float64)
    X = np.zeros(1, dtype=np.float64)
    B = np.array([1.0 / temperature], dtype=np.float64)
    
    # Run the simulation
    model.twoD(spins, E, M, C, X, B)
    
    # Slice off the +2 boundary padding to return only the core 16x16 grid
    return spins[1:-1, 1:-1].copy()

def generate_plot():
    print("Simulating grid states...")
    
    # The three distinct physics phases
    temperatures = [1.5, 2.27, 3.5]
    titles = [
        "Ordered Phase (T=1.5)\nFerromagnetic", 
        "Critical Point (T=2.27)\nPhase Transition", 
        "Disordered Phase (T=3.5)\nParamagnetic"
    ]
    
    # Setup a 1x3 high-resolution plot
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    for ax, T, title in zip(axes, temperatures, titles):
        grid = capture_state(T)
        # Plot the grid: 1 (Up) is black, -1 (Down) is white
        ax.imshow(grid, cmap='binary', vmin=-1, vmax=1)
        ax.set_title(title, pad=15, fontsize=12, fontweight='bold')
        ax.axis('off')
        
    plt.tight_layout()
    output_path = "/data/grid_states.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Success! High-res visualization saved to {output_path}")

if __name__ == "__main__":
    generate_plot()