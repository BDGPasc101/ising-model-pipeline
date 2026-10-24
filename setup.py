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

# Add flags to allow legacy/sloppy C code to compile on modern GCC
legacy_c_flags = [
    '-Wno-implicit-function-declaration', 
    '-Wno-incompatible-pointer-types'
]

ext_modules = [
    Extension(
        "ising",
        sources=["ising/core/ising.pyx", "ising/core/cIsing.c"], 
        include_dirs=[numpy.get_include(), "ising/core"], 
        # Combine the OpenMP flags with the legacy C flags
        extra_compile_args=ompArgs + legacy_c_flags,
        extra_link_args=ompArgs,
    )
]

setup(
    name="ising-simulation",
    version="1.0.0",
    ext_modules=cythonize(ext_modules, compiler_directives={'language_level': "3"}),
)