import os
import random
from multiprocessing import Value, Process


def gen_x_y():
    return random.random(), random.random()


def calc_num_below_curve(func, n, return_value):
    total = 0
    for _ in range(n):
        x, y = gen_x_y()
        if func(x) >= y:
            total += 1
    return_value.value += total


def check_cpu_count(n_requested):
    max_num_cores = os.cpu_count() - 1
    if n_requested > max_num_cores:
        raise Exception(f'Requested too many cores, can only grant {max_num_cores}')


def integrate(func, lower_limit, upper_limit, n_iterations=1000, n_cores=1):
    check_cpu_count(n_cores)
    n_per_core = n_iterations // n_cores
    num_below_curve = Value('i', 0)
    processes = []
    for _ in range(n_cores):
        processes.append(Process(target=calc_num_below_curve, args=(func, n_per_core, num_below_curve)))
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    area = num_below_curve.value / n_iterations
    return area


def main():
    pass


if __name__ == "__main__":
    main()
