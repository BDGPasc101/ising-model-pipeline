import numpy as np
import pytest
from ising_sim import Ising

@pytest.fixture
def base_model():
    """Provides a fresh model instance for each test"""
    return Ising(Ns=8, nPoints=2, eqSteps=10, mcSteps=10)

def test_initialization(base_model):
    """Test that the C-extension initializes memory correctly without crashing"""
    assert base_model is not None, "Model failed to initialize"
    assert type(base_model).__name__ == "Ising", "Model is not the expected Cython class"

def test_array_shapes_and_types(base_model):
    """QA the data pipeline: Ensure the C-code outputs the exact shapes pandas expects"""
    spins = np.zeros((10, 10), dtype=np.int32) # Ns + 2 padding
    E = np.zeros(2, dtype=np.float64)
    M = np.zeros(2, dtype=np.float64)
    C = np.zeros(2, dtype=np.float64)
    X = np.zeros(2, dtype=np.float64)
    B = np.array([1.0, 2.0], dtype=np.float64)

    # Run a tiny simulation
    base_model.twoD(spins, E, M, C, X, B)

    # Invariants: The arrays should remain the same size and not contain NaNs
    assert E.shape == (2,)
    assert not np.isnan(E).any(), "Energy array contains NaN values"
    assert not np.isnan(M).any(), "Magnetization array contains NaN values"
    
    # Physics Invariant: Magnetization per spin can never exceed 1.0 or drop below -1.0
    assert np.all(M <= 1.0)
    assert np.all(M >= -1.0)

def test_deep_freeze_thermodynamics():
    """
    At near-absolute zero (T=0.1), thermal noise is practically non-existent.
    The system should fall into a state of perfect magnetic order (|M| ? 1.0).
    """
    grid_size = 16
    # 500 steps allows the system to settle into a steady state
    model = Ising(grid_size, nPoints=1, eqSteps=500, mcSteps=500)
    
    spins = np.zeros((grid_size + 2, grid_size + 2), dtype=np.int32)
    E = np.zeros(1, dtype=np.float64)
    M = np.zeros(1, dtype=np.float64)
    C = np.zeros(1, dtype=np.float64)
    X = np.zeros(1, dtype=np.float64)
    
    # T = 0.1, therefore Beta (1/T) = 10.0
    B = np.array([1.0 / 0.1], dtype=np.float64) 
    
    model.twoD(spins, E, M, C, X, B)
    
    # The absolute average magnetization per spin must be > 95% aligned
    assert np.abs(M[0]) > 0.95, f"Expected |M| > 0.95 at T=0.1, got {np.abs(M[0])}"


def test_infinite_heat_thermodynamics():
    """
    At extreme heat (T=100.0), thermal noise completely overwhelms any magnetic alignment.
    The spins should flip randomly, canceling each other out to average near zero (|M| ? 0.0).
    """
    grid_size = 16
    model = Ising(grid_size, nPoints=1, eqSteps=500, mcSteps=500)
    
    spins = np.zeros((grid_size + 2, grid_size + 2), dtype=np.int32)
    E = np.zeros(1, dtype=np.float64)
    M = np.zeros(1, dtype=np.float64)
    C = np.zeros(1, dtype=np.float64)
    X = np.zeros(1, dtype=np.float64)
    
    # T = 100.0, therefore Beta (1/T) = 0.01
    B = np.array([1.0 / 100.0], dtype=np.float64) 
    
    model.twoD(spins, E, M, C, X, B)
    
    # The absolute average magnetization per spin must be near 0
    assert np.abs(M[0]) < 0.2, f"Expected |M| < 0.2 at T=100.0, got {np.abs(M[0])}"    

def test_c_extension_type_safety(base_model):
    """
    Prove that passing the wrong data type (float instead of int) 
    is safely caught by Cython, preventing a C-level segfault.
    """
    # The C-code strictly expects np.int32 for the spins grid.
    # We deliberately pass np.float64 to attempt to break the memory mapping.
    bad_spins = np.zeros((10, 10), dtype=np.float64) 
    
    E = np.zeros(2, dtype=np.float64)
    M = np.zeros(2, dtype=np.float64)
    C = np.zeros(2, dtype=np.float64)
    X = np.zeros(2, dtype=np.float64)
    B = np.array([1.0, 2.0], dtype=np.float64)

    # Cython should intercept this and raise a TypeError or ValueError
    with pytest.raises((TypeError, ValueError)):
        base_model.twoD(bad_spins, E, M, C, X, B)


def test_c_extension_shape_safety(base_model):
    """
    Prove that passing mismatched array dimensions is intercepted safely.
    """
    spins = np.zeros((10, 10), dtype=np.int32)
    E = np.zeros(2, dtype=np.float64)
    
    # Magnetization (M) expects a 1D array of size 2. 
    # We deliberately pass a 2D array to try to break the C loop.
    bad_M = np.zeros((2, 2), dtype=np.float64) 
    
    C = np.zeros(2, dtype=np.float64)
    X = np.zeros(2, dtype=np.float64)
    B = np.array([1.0, 2.0], dtype=np.float64)

    # Cython should intercept the dimension mismatch and raise a ValueError
    with pytest.raises(ValueError):
        base_model.twoD(spins, E, bad_M, C, X, B)