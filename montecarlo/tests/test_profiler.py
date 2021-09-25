import unittest
from montecarlo.profiler import profiler
import time


class ProfilerTest(unittest.TestCase):
    def test_time_function_timing(self):
        def sleep_two(*args, **kwargs):
            time.sleep(2)
            return None
        none_value, time_value = profiler.time_function(sleep_two)
        self.assertAlmostEqual(time_value, 2, 1)

    def test_calc_relative_err(self):
        self.assertAlmostEqual(profiler.calc_relative_err(2, 0), 1)
        self.assertAlmostEqual(profiler.calc_relative_err(-2, 0), 1)
        self.assertAlmostEqual(profiler.calc_relative_err(100, 2), .98)


if __name__ == "__main__":
    unittest.main()
