import numpy as np
import pandas as pd
# Import the Cython module we just compiled!
from ising_sim import Ising  

def run_experiment():
    print("Starting Ising Model Simulation...")
    
    # 1. Define simulation parameters
    grid_size = 16
    n_points = 20  # Number of temperature points to simulate
    eq_steps = 1000
    mc_steps = 1000
    
    # 2. Initialize the Cython class (Ns, nPoints, eqSteps, mcSteps)
    model = Ising(grid_size, n_points, eq_steps, mc_steps)
    
    # 3. Create the NumPy arrays required by the C code
    # Spin grid needs padding (N+2) for periodic boundary conditions
    spins = np.zeros((grid_size + 2, grid_size + 2), dtype=np.int32)
    
    # Arrays to hold the output data
    energy = np.zeros(n_points, dtype=np.float64)
    magnetization = np.zeros(n_points, dtype=np.float64)
    specific_heat = np.zeros(n_points, dtype=np.float64)
    susceptibility = np.zeros(n_points, dtype=np.float64)
    
    # Beta values (Inverse temperature: 1/T). 
    # The phase transition for a 2D Ising model happens around T=2.269
    temperatures = np.linspace(1.5, 3.5, n_points)
    beta_values = (1.0 / temperatures).astype(np.float64)
    
    # 4. Run the high-performance C simulation
    print(f"Running {mc_steps} Monte Carlo steps across {n_points} temperatures...")
    model.twoD(spins, energy, magnetization, specific_heat, susceptibility, beta_values)
    
    # 5. Build the Data Pipeline using pandas
    print("Simulation complete. Structuring data...")
    results_df = pd.DataFrame({
        'Temperature': temperatures,
        'Beta': beta_values,
        'Energy': energy,
        'Magnetization': np.abs(magnetization), # Use absolute magnetization
        'Specific_Heat': specific_heat,
        'Susceptibility': susceptibility
    })
    

    # Change the output file path at the bottom
    output_file = "/data/simulation_results.csv"
    results_df.to_csv(output_file, index=False)
    print(f"\nSuccess! Data saved to {output_file}")
    print(results_df.head())

if __name__ == "__main__":
    run_experiment()