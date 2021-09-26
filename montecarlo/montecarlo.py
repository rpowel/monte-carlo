import os
import random
from multiprocessing import Value, Process


def _gen_x_y(lower_limit, upper_limit):
    if upper_limit <= lower_limit:
        raise ValueError("Upper limit must be higher than lower limit")
    diff = abs(upper_limit - lower_limit)
    return random.random()*diff + min([lower_limit, upper_limit]), random.random()


def _calc_num_below_curve(func, lower_limit, upper_limit, num_points, return_value):
    total = 0
    for _ in range(num_points):
        x, y = _gen_x_y(lower_limit, upper_limit)
        if func(x) >= y:
            total += 1
    return_value.value += total


def _check_cpu_count(num_cores_requested):
    max_num_cores = os.cpu_count() - 1
    if num_cores_requested > max_num_cores:
        raise Exception(f'Requested too many cores, can only grant {max_num_cores}.')
    elif num_cores_requested < 1:
        raise Exception(f'Requested too few cores, must request at least one core.')


def integrate(func, lower_limit, upper_limit, num_iterations=1000, num_cores=1):
    _check_cpu_count(num_cores)
    num_points_per_core = int(num_iterations // num_cores)
    num_below_curve = Value('i', 0)
    processes = []
    for i in range(num_cores):
        processes.append(
            Process(
                target=_calc_num_below_curve,
                args=(
                    func,
                    lower_limit,
                    upper_limit,
                    num_points_per_core,
                    num_below_curve
                )
            )
        )
        processes[i].start()
    for p in processes:
        p.join()
    area = num_below_curve.value / num_iterations
    return area
