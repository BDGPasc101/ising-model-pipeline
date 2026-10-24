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