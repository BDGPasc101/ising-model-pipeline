# ising-model-pipeline
Ising model adapted for learning purposes - based on original work https://github.com/rajeshrinet/compPhy

My goals:
- Transfer the original model for producing plots for the Ising model, including the main file ising.pyx
- Clean up files and dependencies
- Create a dockerfile
- Create pyTest suite

Suggested steps from Gemini:
1. Fix the "Dependency Hell" (The Build Pipeline)
Look at lines 16-18: cdef extern from "../../misc/mt19937ar.c".
The scientist hardcoded a relative path to a custom random number generator written in C. If anyone downloads this folder without the misc folder exactly two directories up, the compilation will fail.

Your Fix: Create a proper setup.py file to handle the Cython compilation cleanly. Bundle the necessary C dependencies directly into the module's directory so it is self-contained.

2. Containerize the Compilation (Docker)
Cython requires a C compiler (like GCC), Python headers, and NumPy headers to build successfully. This is notoriously difficult to set up on Windows or macOS natively.

Your Fix: Write a Dockerfile that uses a slim Python base image, installs build-essential (for the C compiler), installs numpy and cython, and automatically compiles this .pyx file into a usable Python library when the container builds. This makes the simulation "1-click" reproducible for anyone.

3. Build a Modern Data Pipeline (pandas)
Look at cpdef twoD. It takes empty arrays (E, M, C, X for Energy, Magnetization, Specific Heat, and Susceptibility) and populates them in memory. It has no mechanism for saving this data.

Your Fix: Write a clean Python wrapper script (run_simulation.py).

Import the compiled Cython module.

Pass in the parameters (grid size, temperatures, steps).

Take the resulting E, M, C, X NumPy arrays and load them into a pandas DataFrame.

Save the DataFrame to a modern, compressed format like Parquet or CSV.

4. Apply Your QA Superpower (Pytest)
This code has complex array bounds checking (e.g., S[0, b] = S[N, b]) to handle periodic boundary conditions (making the grid act like a torus/donut so the edges wrap around). This is highly prone to "off-by-one" errors.

Your Fix: Write a pytest suite.

Math Tests: At very high temperatures, Magnetization should average out to 0. At very low temperatures, it should lock at 1 or -1. Write a test that runs a tiny grid and asserts these thermodynamic laws hold true.

Logic Tests: Write a unit test for calcEnergy passing in a grid of all 1s (all spins pointing up). The energy should equal exactly -2 * N * N.

5. Create the CI/CD Workflow
Set up a .github/workflows/main.yml file. Configure it so that every time you push code, GitHub Actions builds your Docker container, compiles the Cython C-extensions, and runs your pytest suite.

If you build this, a hiring manager at a national lab will see someone who knows how to take their complex computational physics (Cython/C++), make it robust (Pytest), make it reproducible (Docker), and integrate it into modern data tools (pandas).

Progress log with reasoning:
