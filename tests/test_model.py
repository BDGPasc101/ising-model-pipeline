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