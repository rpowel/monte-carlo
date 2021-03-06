import unittest
from montecarlo import montecarlo
from multiprocessing import Value


def triangle_func(x):
    return x


def flat_line_at_one(_):
    return 1


def flat_line_at_zero(_):
    return 0


class MonteCarloTest(unittest.TestCase):
    def test_gen_x_y(self):
        range_list = [(0, 1), (0, 10), (-10, 0), (-10, 10)]
        for lower, upper in range_list:
            x, y = montecarlo._gen_x_y(lower, upper)
            self.assertGreaterEqual(x, lower)
            self.assertLessEqual(x, upper)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(y, 1)
        with self.assertRaises(ValueError) as context:
            _, _ = montecarlo._gen_x_y(10, 0)
        self.assertTrue('must be higher' in str(context.exception))

    def test_calc_num_below_curve_all(self):

        num_points = 100
        num_below = Value('i', 0)
        montecarlo._calc_num_below_curve(flat_line_at_one, 0, 1, num_points, num_below)
        self.assertEqual(num_below.value, num_points)

    def test_calc_num_below_curve_none(self):
        num_points = 100
        num_below = Value('i', 0)
        montecarlo._calc_num_below_curve(flat_line_at_zero, 0, 1, num_points, num_below)
        self.assertEqual(num_below.value, 0)

    def test_calc_num_below_curve_half(self):
        num_points = 1000000
        num_below = Value('i', 0)
        montecarlo._calc_num_below_curve(triangle_func, 0, 1, num_points, num_below)
        self.assertAlmostEqual(num_below.value/num_points, 0.5, 2)

    def test_check_cpu_count_low(self):
        with self.assertRaises(Exception) as context:
            montecarlo._check_cpu_count(0)
        self.assertTrue('too few cores' in str(context.exception))

    def test_check_cpu_count_high(self):
        with self.assertRaises(Exception) as context:
            montecarlo._check_cpu_count(1000)
        self.assertTrue('too many cores' in str(context.exception))

    def test_check_cpu_count_normal(self):
        self.assertIsNone(montecarlo._check_cpu_count(1))

    def test_integrate(self):
        area = montecarlo.integrate(triangle_func, 0, 1, 100000, num_cores=1)
        self.assertAlmostEqual(area, 0.5, 2)


if __name__ == '__main__':
    unittest.main()
