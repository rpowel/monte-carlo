# Monte Carlo
Calculate the integral of arbitrary, finite, real functions over a finite interval using a
Monte Carlo methodology. This method allows for selection of number of Monte Carlo guesses
to use as well as the number of CPU cores to utilize (up to <available_cores>-1).

## Installation
Clone git repo:
```shell
$ git clone https://github.com/rpowel/monte-carlo
```
Install python dependencies:
```shell
$ cd monte-carlo
$ pip install -r requirements.txt
```

## Usage
```python
from montecarlo.montecarlo import integrate

# Integration limits
LOWER_LIMIT = 0
UPPER_LIMIT = 1

# Monte-Carlo kwargs
NUM_ITERATIONS = 10000
NUM_CORES = 2

# Define your function to integrate
def function_to_integrate(x):
    return x**2

# Calculate area under the curve
area = integrate(
    function_to_integrate,
    LOWER_LIMIT,
    UPPER_LIMIT,
    num_iterations=NUM_ITERATIONS,
    num_cores=NUM_CORES,
)
# Returns ~0.5
# Accuracy depends on NUM_ITERATIONS
```

## Profiling
Test the accuracy and speed curves of integration on your function:
```python
from montecarlo import montecarlo
from montecarlo.profiler import profiler

# Integration limits
LOWER_LIMIT = 0
UPPER_LIMIT = 1

# Profiling kwargs
CORES_LOW = 1  # Lower limit of cores to test
CORES_HIGH = 4  # Upper limit of cores to test
ITER_LOW = 100  # Lower limit of iterations
ITER_HIGH = 1e6  # Upper limit of iterations

# Define your function to integrate
def function_to_integrate(x):
    return x**2

    
def calculate_area(num_iterations=1000, num_cores=1):
    area = montecarlo.integrate(
        function_to_integrate,
        LOWER_LIMIT,
        UPPER_LIMIT,
        num_iterations=num_iterations,
        num_cores=num_cores,
    )
    return area

profiler.profile(
    calculate_area,
    cores_low=CORES_LOW,
    cores_high=CORES_HIGH,
    iter_low=ITER_LOW,
    iter_high=ITER_HIGH,
)
```

## Testing
Unit tests are defined in `montecarlo/tests/` and can be run all together from the project root directory with:
```shell
$ python -m unittest discover montecarlo/tests
```
