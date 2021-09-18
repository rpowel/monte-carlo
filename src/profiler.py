import time
import json
import numpy as np
import matplotlib.pyplot as plt
from calculate_pi import calculate_pi


with open('profiler_defaults.json', 'r') as defaults_json:
    DEFAULT_VALUES = json.load(defaults_json)


def time_function(func, **kwargs):
    t1 = time.time()
    value = func(
        num_iterations=kwargs.get('num_iterations', DEFAULT_VALUES['num_iterations']),
        num_cores=kwargs.get('num_cores', DEFAULT_VALUES['num_cores']),
    )
    t2 = time.time()
    return value, abs(t2-t1)


def calc_relative_err(ideal_value, calculated_list):
    calculated_list = np.asarray(calculated_list)
    return abs(calculated_list - ideal_value) / ideal_value


def profile_num_iterations(func, **kwargs):
    iter_list = []
    value_list = []
    time_list = []
    num_iterations = kwargs.get('iter_low', DEFAULT_VALUES['iter_low'])
    while num_iterations < kwargs.get('iter_high', DEFAULT_VALUES['iter_high']):
        iter_list.append(num_iterations)
        value, time_ = time_function(func, num_iterations=num_iterations)
        value_list.append(value)
        time_list.append(time_)
        num_iterations *= 10
    iter_list = np.asarray(iter_list)
    value_list = np.asarray(value_list)
    time_list = np.asarray(time_list)
    return iter_list, value_list, time_list


def profile_num_cores(func, **kwargs):
    iter_list = []
    value_list = []
    time_list = []
    num_cores = kwargs.get('cores_low', DEFAULT_VALUES['cores_low'])
    while num_cores < kwargs.get('cores_high', DEFAULT_VALUES['cores_high']):
        iter_list.append(num_cores)
        value, time_ = time_function(func, num_cores=num_cores)
        value_list.append(value)
        time_list.append(time_)
        num_cores += 1

    iter_list = np.asarray(iter_list)
    value_list = np.asarray(value_list)
    time_list = np.asarray(time_list)
    return iter_list, value_list, time_list


def plot_err_curve(ideal_value, ind_var_list, value_list, time_list, **kwargs):
    err_list = calc_relative_err(ideal_value, value_list)

    plt.loglog(ind_var_list, err_list, c='C0', alpha=0.7, label='Monte-Carlo')

    plt.xlabel('Number of Iterations')
    plt.ylabel('Relative Error')
    plt.tight_layout()

    plt.show()


def gen_profile_curves(ideal_value, func_to_integrate, **kwargs):
    num_iter_list, value_iter_list, time_iter_list = profile_num_iterations(
        func_to_integrate,
        iter_high=kwargs.get('iter_high', DEFAULT_VALUES['iter_high']),
        iter_low=kwargs.get('iter_low', DEFAULT_VALUES['iter_low']),
        num_cores=kwargs.get('num_cores', DEFAULT_VALUES['num_cores']),
    )
    print(value_iter_list)
    plot_err_curve(ideal_value, num_iter_list, value_iter_list, time_iter_list)
    num_cores_list, value_cores_list, time_cores_list = profile_num_cores(
        func_to_integrate,
        cores_low=kwargs.get('cores_low', DEFAULT_VALUES['cores_low']),
        cores_high=kwargs.get('cores_high', DEFAULT_VALUES['cores_high']),
        num_iterations=kwargs.get('num_iterations', DEFAULT_VALUES['num_iterations']),
    )
    plot_err_curve(ideal_value, num_cores_list, value_cores_list, time_cores_list)


def main():
    gen_profile_curves(np.pi, calculate_pi, num_cores=10, iter_high=1e10)


if __name__ == "__main__":
    main()
