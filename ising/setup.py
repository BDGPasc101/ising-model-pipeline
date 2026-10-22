import numpy
import os, tempfile, subprocess, shutil
from setuptools import setup, Extension
from Cython.Build import cythonize

def checkOpenmpSupport():
    """ 
    Programmatically testing for OpenMP support from a Python setup script
    """ 
    ompTest = \
    r"""
    #include <omp.h>
    #include <stdio.h>
    int main() {
    #pragma omp parallel
    printf("Thread %d, Total number of threads %d\n", omp_get_thread_num(), omp_get_num_threads());
    }
    """
    tmpdir = tempfile.mkdtemp()
    curdir = os.getcwd()
    os.chdir(tmpdir)

    filename = r'test.c'
    with open(filename, 'w') as file:
        file.write(ompTest)
    with open(os.devnull, 'w') as fnull:
        result = subprocess.call(['cc', '-fopenmp', filename],
                                 stdout=fnull, stderr=fnull)

    os.chdir(curdir)
    shutil.rmtree(tmpdir) 
    if result == 0:
        return True
    else:
        return False

# Determine OpenMP arguments
ompArgs = ['-fopenmp'] if checkOpenmpSupport() else []

ext_modules = [
    Extension(
        "ising",
        # We explicitly add all .c files here so they compile together
        sources=["core/ising.pyx", "core/cIsing.c", "core/mt19937ar.c"], 
        include_dirs=[numpy.get_include(), "core"], 
        extra_compile_args=ompArgs,
        extra_link_args=ompArgs,
    )
]

setup(
    name="ising-simulation",
    version="1.0.0",
    # cythonize() replaces the old cmdclass dictionary
    ext_modules=cythonize(ext_modules, compiler_directives={'language_level': "3"}),
)