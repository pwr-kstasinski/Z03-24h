import unittest
import solution


class TestCalculations(unittest.TestCase):

    def test_results(self):
        equation1 = solution.Equation('1+2*3')
        self.assertEqual(equation1.calculate_result(), 7)
        equation2 = solution.Equation('3+((5+9)*2)')
        self.assertEqual(equation2.calculate_result(), 31)
        equation3 = solution.Equation('(0.5+10*2-(5+0.1*3))*0.5+0.35')
        self.assertAlmostEqual(equation3.calculate_result(), 7.95)


if __name__ == '__main__':
    unittest.main()
