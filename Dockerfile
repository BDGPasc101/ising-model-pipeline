# 1. Use a lightweight Python base image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Install system-level C compilers and OpenMP libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# 4. Install Python build dependencies
# NumPy must be installed before running setup.py because setup.py imports it
RUN pip install --no-cache-dir numpy cython pandas pytest

# 5. Copy the necessary project files into the container
COPY setup.py .
COPY ising/ ./ising/
COPY run_simulation.py .

# 6. Compile the Cython extension
RUN python setup.py build_ext --inplace

# 7. Default command (drops you into a Python shell or runs a specific script)
CMD ["python"]