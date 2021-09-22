import unittest
from montecarlo import montecarlo
from multiprocessing import Value


def triangle_func(x):
    return x


def flat_line_at_one(x):
    return 1


def flat_line_at_zero(x):
    return 0


class MonteCarloTest(unittest.TestCase):
    def test_gen_x_y(self):
        x, y = montecarlo._gen_x_y()
        self.assertGreaterEqual(x, 0)
        self.assertGreaterEqual(y, 0)
        self.assertLessEqual(x, 1)
        self.assertLessEqual(y, 1)

    def test_calc_num_below_curve_all(self):

        num_points = 100
        num_below = Value('i', 0)
        montecarlo._calc_num_below_curve(flat_line_at_one, num_points, num_below)
        self.assertEqual(num_below.value, num_points)

    def test_calc_num_below_curve_none(self):
        num_points = 100
        num_below = Value('i', 0)
        montecarlo._calc_num_below_curve(flat_line_at_zero, num_points, num_below)
        self.assertEqual(num_below.value, 0)

    def test_calc_num_below_curve_half(self):
        num_points = 1000000
        num_below = Value('i', 0)
        montecarlo._calc_num_below_curve(triangle_func, num_points, num_below)
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
