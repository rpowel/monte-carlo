import os
import random
from typing import Callable
from multiprocessing import Value, Process


def _gen_x_y(lower_limit: float, upper_limit: float) -> (float, float):
    """
    Generate random x, and y for given range of integration.
    :param lower_limit: float
    Lower limit of integration.
    :param upper_limit: float
    Upper limit of integration.
    :return: (x, y)
    """
    if upper_limit <= lower_limit:
        raise ValueError("Upper limit must be higher than lower limit")
    diff = abs(upper_limit - lower_limit)
    return random.random() * diff + min([lower_limit, upper_limit]), random.random()


def _calc_num_below_curve(
        func: Callable[[float], float],
        lower_limit: float,
        upper_limit: float,
        num_iterations: int,
        return_value: type(Value),
) -> None:
    """
    Calculate number of points below curve from total number of points to check.
    :param func: Callable
    Function to integrate.
    :param lower_limit: float
    Lower limit of integration.
    :param upper_limit: float
    Upper limit of integration.
    :param num_iterations: int
    Number of iterations to run through monte-carlo to check if below curve.
    :param return_value: multiprocessing.Value
    Value containing number of points counted as below curve by all processors.
    :return: None
    """
    total = 0
    for _ in range(num_iterations):
        x, y = _gen_x_y(lower_limit, upper_limit)
        if func(x) >= y:
            total += 1
    return_value.value += total


def _check_cpu_count(num_cores_requested: int) -> None:
    """
    Check requested cores against available logical processors. Raise exception if more than `<available>-1`.
    :param num_cores_requested: int
    Number of cores requested.
    :return: None
    """
    max_num_cores = os.cpu_count() - 1
    if num_cores_requested > max_num_cores:
        raise Exception(f'Requested too many cores, can only grant {max_num_cores}.')
    elif num_cores_requested < 1:
        raise Exception(f'Requested too few cores, must request at least one core.')


def integrate(
        func: Callable[[float], float],
        lower_limit: float,
        upper_limit: float,
        num_iterations: int = 1000,
        num_cores: int = 1
) -> float:
    """
    Numerically integrate arbitrary function over finite range.
    :param func: Callable
    Function to integrate. Must take only one argument and return one value. i.e. f(x) return y.
    :param lower_limit: float
    Lower limit of integration.
    :param upper_limit: float
    Upper limit of integration.
    :param num_iterations: int
    Number of points to check in monte-carlo scheme.
    Error is related to num_iterations, so points will be more accurate, but will slow down calculation.
    :param num_cores: int
    Number of cores to use for calculation.
    Python takes time to start new proccesses so for small `num_iterations` fewer cores is better.
    :return:
    Area under curve for given integration range.
    """
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
