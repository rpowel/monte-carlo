import time
import json
import numpy as np
import matplotlib.pyplot as plt
from montecarlo.tests.calculate_pi import calculate_pi

profiler_path = str(__file__)
profiler_defaults_path = '/'.join(profiler_path.split('\\')[:-1]) + '/profiler_defaults.json'
with open(profiler_defaults_path, 'r') as defaults_json:
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
    return abs((calculated_list - ideal_value) / ideal_value)


def profile_num_cores(func, **kwargs):
    iter_low = kwargs.get('iter_low', DEFAULT_VALUES['iter_low'])
    iter_high = kwargs.get('iter_high', DEFAULT_VALUES['iter_high'])
    num_iter_list = np.logspace(
        int(np.log10(iter_low)),
        int(np.log10(iter_high)),
        num=2*int((np.log10(iter_high) - np.log10(iter_low))),
        dtype=int,
    )
    cores_low = kwargs.get('cores_low', DEFAULT_VALUES['cores_low'])
    cores_high = kwargs.get('cores_high', DEFAULT_VALUES['cores_high'])
    num_cores_list = np.arange(cores_low, cores_high+1, 1, dtype=int)

    values_list = np.zeros([num_cores_list.size, num_iter_list.size])
    times_list = np.zeros([num_cores_list.size, num_iter_list.size])

    for i, num_cores in enumerate(num_cores_list):
        for j, num_iterations in enumerate(num_iter_list):
            values_list[i, j], times_list[i, j] = time_function(
                func,
                num_iterations=num_iterations,
                num_cores=num_cores,
            )

    return num_iter_list, num_cores_list, values_list, times_list


def plot_err_curve(ideal_value, ind_var_list, value_list):
    err_list = calc_relative_err(ideal_value, value_list)

    plt.loglog(ind_var_list, err_list, c='C0', alpha=0.7, label='Monte-Carlo')
    plt.xlabel('Number of Iterations')
    plt.ylabel('Relative Error')
    plt.tight_layout()

    plt.show()


def plot_single_time_curve(num_iter_list, time_list, num_cores):
    plt.plot(num_iter_list, time_list, label=f'{num_cores} Cores')


def plot_all_time_curves(num_iter_list, time_list, num_cores_list, **kwargs):
    for i, (times, num_cores) in enumerate(zip(time_list, num_cores_list)):
        plot_single_time_curve(num_iter_list, times, num_cores)

    plt.xscale('log')
    plt.yscale('log')
    plt.grid(alpha=0.4)

    plt.ylabel(kwargs.get('ylabel', 'Time (s)'))
    plt.xlabel(kwargs.get('xlabel', 'Number of Iterations'))
    plt.title(kwargs.get('title', 'Calculation Time'))

    plt.tight_layout()
    plt.legend(loc=0)
    plt.show()


def gen_cores_profile_plots(func_to_integrate, **kwargs):
    num_iter_list, num_cores_list, values_list, times_list = profile_num_cores(func_to_integrate, **kwargs)
    plot_all_time_curves(
        num_iter_list,
        times_list,
        num_cores_list,
        title=f"Calculation Time vs. Number of Cores Used",
        xlabel="Number of Iterations",
        ylabel="Time (s)",
    )


def profile(func, **kwargs):
    gen_cores_profile_plots(func, **kwargs)


if __name__ == "__main__":
    profile(calculate_pi, cores_low=1, cores_high=3, iter_low=100, iter_high=1e7)
