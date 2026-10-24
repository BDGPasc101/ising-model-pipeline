Modernising the setup file:


Docker:
Create a file named Dockerfile in the root of your project (right next to your setup.py).

This Dockerfile acts as the blueprint to create a pristine Linux environment, install the C compiler, pull down the necessary Python libraries, and compile your Cython code natively.

Note - Important to installed recommended "Container Tools" for docker if prompted. Helps to build out dockerfile by denoting spelling errors and syntax issues. Also helps with a UI tool to manager contains and images. Can right click the dockerfile to build the image directly from the side menu.


Error encountered when trying to run docker:
"2.244 ising/core/cIsing.c:67:14: err: implicit declaration of fn ?total_energy? [-Wimplicit-function-declaration]
2.244    67 |         E0 = total_energy(Spin, Nsites);
2.244       |              ^~~~~~~~~~~~
2.244 ising/core/cIsing.c:11:9: note: prev declaration of ?total_energy? with type ?int(int *, int)?
2.244    11 |     int total_energy(int [],         int );
2.244       |         ^~~~~~~~~~~~"
Coach: "This error is a textbook example of why Research Software Engineers are needed. The original scientist wrote sloppy, older C code (calling a function total_energy without properly declaring it according to modern C standards). The modern GCC compiler inside your pristine Docker environment caught the sloppy code and threw a fatal error (-Wimplicit-function-declaration).

As an RSE, your goal is not to rewrite their 10-year-old C code (which risks breaking the math). Your goal is to fix the build system to accommodate it."

Fix: Add compiler flags to setup file to reduce harshness of C checks

Next docker compile error:
"When the original scientist ran Cython years ago, it translated their .pyx file into a massive C file (ising.c) and they accidentally committed that generated C file to their GitHub repository along with the source code.

Because ising.c is already sitting in your folder, your setup.py script sees it and says, "Oh, it's already translated, I'll just pass this directly to the GCC compiler!" That old ising.c still contains the hardcoded ../../misc paths, completely ignoring the fixes you made to the .pyx file."

Fix:  Remove stale file, change random number generator paths in ising.pyx file

The Linker in C Compilation
- tbc

Upon successful docker compilation, you can see "ising.cpython-311-x86_64-linux-gnu.so. That .so file is a compiled "Shared Object."" - I can also see an image present in docker desktop itself.

Creating the run simulation python script - Pandas and NumPy
Naming the arrays
- If you look at line 37 in the ising.pyx file you pasted, you will see the function signature for running the 2D simulation: "cpdef twoD(self, int [:, :] S, double [:] E, double [:] M, double [:] C, double [:] X, double [:] B):"

"Here is exactly how those Cython definitions translate into the Python/NumPy arrays we created:
1. The Data Types (Memoryviews)
Cython uses "typed memoryviews" to talk to C arrays rapidly:
int [:, :]: This means a 2-dimensional array of integers (dtype=np.int32).
double [:]: This means a 1-dimensional array of double-precision floats (dtype=np.float64).
2. The Physics Variables (E, M, C, X, B)
By looking at the math happening inside the twoD loop, we can map the single letters to standard statistical mechanics terminology:
E (Energy): On line 63, E1 = E1 + Ene where Ene = calcEnergy().
M (Magnetization): On line 64, M1 = M1 + Mag where Mag = calcMag().
C (Specific Heat): On line 69, C[tt] is calculated using the variance in energy (E2 - E1*E1). In statistical physics, the fluctuation in energy defines a system's Specific Heat Capacity.
X (Susceptibility): On line 70, X[tt] uses the variance in magnetization (M2 - M1*M1). This defines Magnetic Susceptibility (often denoted by the Greek letter $\chi$, hence the X).
B (Beta): On line 46, beta = B[tt]. In physics, $\beta = 1/T$ (inverse temperature).3. The Grid Size Padding (The S array)
The spins array (S) was defined as np.zeros((grid_size + 2, grid_size + 2)).
This requirement comes from lines 52-53 in ising.pyx:
Code snippet
S[0, b]   = S[N, b];  S[N+1, b] = S[1, b];  # ensuring BC
S[a, 0]   = S[a, N];  S[a, N+1] = S[a, 1];
"BC" stands for Boundary Conditions. The physics model treats the grid like a torus (a donut) so the edges wrap around. To calculate the math without crashing at the edges, the C code requires a "halo" or padding of 1 extra cell on all four sides of the $N \times N$ grid, which is why the array size must be $N+2$."

Running the simulation and retrieving accessible output data:
"To run the simulation and save the CSV back to your Windows machine, use a Docker Volume Mount (-v)."
docker run --rm -v ${PWD}:/app ising-model python run_simulation.py

Error: Shadowing trap - C code was compiled inside container so file could not be found when windows files mounting occured
Python naming collision: Could not find "Ising" class inside the directory

Fix: update name to "ising_sim" for import, save output to dedicated data folder. Ensure script for simulation is added to dockfile

Cleaning up ising.pyx - defunct import for unused function
Coach: "If you look at the original ising.pyx file around line 9, the scientist wrote import matplotlib.pyplot as plt.

However, if you read through the rest of the math in that file, they never actually use plt anywhere. It is a dead import left over from when they were prototyping.

As a Research Software Engineer, you know that a core, high-performance C-extension should never handle its own plotting. Computation and visualization should always be strictly separated. Adding matplotlib to your Dockerfile would just bloat your container image size by ~100MB for no reason."

