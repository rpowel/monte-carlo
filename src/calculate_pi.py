from monte_carlo import integrate
from math import sqrt


def quarter_circle(x):
    y = sqrt(1 - x**2)
    return y


def calculate_pi(num_iterations=10000, num_cores=1):
    pi = 4 * integrate(quarter_circle, 0, 1, num_iterations=num_iterations, num_cores=num_cores)
    return pi


def main():
    num_iter = 100000
    num_cores = 1
    pi = calculate_pi(num_iterations=num_iter, num_cores=num_cores)
    print(pi)


if __name__ == "__main__":
    main()
