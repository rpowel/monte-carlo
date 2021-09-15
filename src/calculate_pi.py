from monte_carlo import integrate
from math import sqrt
import time


def quarter_circle(x):
    y = sqrt(1 - x**2)
    return y


def calculate_pi(n_iterations=10000, n_cores=1):
    pi = 4 * integrate(quarter_circle, 0, 1, n_iterations=n_iterations, n_cores=n_cores)
    return pi


def main():
    n_iter = 100000
    n_cores = 1
    pi = calculate_pi(n_iterations=n_iter, n_cores=n_cores)
    print(pi)


if __name__ == "__main__":
    main()
