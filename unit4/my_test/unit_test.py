import unittest
from circle_main import circle
from circle_main import Total_R_Square, Max_Radius


class Circle_Test(unittest.TestCase):
    def setUp(self):
        self.c1 = circle(+0.5, +0.5, +0.5)
        self.c2 = circle(-0.5, +0.5, +0.5)
        self.c3 = circle(-0.5, -0.5, +0.5)
        self.c4 = circle(+0.5, -0.5, +0.5)
        self.c_list = []
        self.c1.Append_To(self.c_list)
        self.c2.Append_To(self.c_list)
        self.c3.Append_To(self.c_list)
        self.c4.Append_To(self.c_list)

    def test_In_Range(self):
        self.assertTrue(self.c1.In_Range())

    def test_R_Square(self):
        R_true = 4 * (0.5**2)
        R_test = Total_R_Square(self.c_list)
        self.assertEqual(R_true, R_test)

    def test_Distance(self):
        D_true = 0
        D_test = self.c1.Distance(self.c2)
        self.assertEqual(D_true, D_test)


if __name__ == "__main__":
    unittest.main()
