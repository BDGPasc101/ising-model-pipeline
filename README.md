![CI/CD Pipeline](https://github.com/BDGPasc101/ising-model-pipeline/actions/workflows/ci.yml/badge.svg)
# ⚛️ Ising Model Pipeline: Legacy C to Modern Data Pipeline

A modernized, containerized, and fully tested computational physics pipeline simulating the 2D Ising Model phase transition. 

Based on original Cython/C work from [rajeshrinet/compPhy](https://github.com/rajeshrinet/compPhy), this repository has been re-architected to demonstrate best practices in Research Software Engineering (RSE).

---

## 🎯 Portfolio Project Goals

This project was built to demonstrate the transition of a complex, academic computational physics model into a robust software engineering pipeline. 

**Core Objectives:**
1. **Solve "Dependency Hell":** Containerize the C/Cython compilation process to guarantee cross-platform reproducibility without manual compiler configuration.
2. **Modernize the Build System:** Refactor legacy Cython implementations, fix hardcoded relative paths, resolve linker collisions, and package the C-extension using standard `setup.py` and `pip`.
3. **Build a Data Pipeline:** Decouple computation from visualization. Use the high-performance C-binary for the Monte Carlo simulation, passing the output into a modern Python data stack (`pandas`, `matplotlib`).
4. **Apply QA Superpowers:** Introduce a robust automated testing suite (`pytest`) to validate memory initialization, data array invariants, and the thermodynamic laws governing the model.

---

## 📊 The Physics: Phase Transitions

The Ising Model simulates ferromagnetism using a 2D grid of atomic "spins". The simulation uses Monte Carlo methods to model the competition between magnetic alignment (order) and thermal energy (chaos).

As temperature increases, the model correctly predicts a critical phase transition ($T_c \approx 2.269$) where the material loses its magnetization—melting from a solid magnet into a disordered state.

*(Note: Add your `data/grid_states.png` here in GitHub to show the visual transition from Ordered → Critical → Disordered).*

---

## 🛠️ Architecture & Engineering Highlights

*   **Cython/C Integration:** The computationally heavy Monte Carlo steps and Mersenne Twister random number generation are executed purely in C for maximum performance, exposed to Python via a compiled `.so` extension (`ising_sim`).
*   **Dockerized Environment:** The entire build and runtime environment is encapsulated in a `Python 3.11-slim` Docker image, complete with GCC and necessary headers.
*   **Data Extraction:** The Python layer orchestrates the C-extension, extracts multi-dimensional memoryviews into NumPy arrays, and exports structured datasets to `data/simulation_results.csv`.
*   **Automated Testing:** Pytest validates the C-extension's memory safety, array shapes, and bounds constraints without exposing fragile internal C declarations.

---

## 🚀 Quick Start

Reproduce the exact simulation environment instantly using Docker.

**1. Build the compilation environment:**
```bash
docker build -t ising-model .
```

**2. Run the data pipeline (outputs to `/data`):**
```bash
docker run --rm -v ${PWD}/data:/data ising-model python /app/run_simulation.py
```

**3. Generate the grid state visualizations:**
```bash
docker run --rm -v ${PWD}/data:/data -v ${PWD}/visualise_grids.py:/app/visualise_grids.py ising-model python /app/visualise_grids.py
```

**4. Run the QA Test Suite:**
```bash
docker run --rm ising-model pytest tests/ -v -s --tb=short
```