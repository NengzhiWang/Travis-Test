import unittest
from circle_main import circle
from circle_main import Total_R_Square, Max_Radius


class Circle_Test(unittest.TestCase):
    def init(self):
        self.c1 = circle(+0.5, +0.5, +0.5)
        self.c2 = circle(-0.5, +0.5, +0.5)
        self.c3 = circle(-0.5, -0.5, +0.5)
        self.c4 = circle(+0.5, -0.5, +0.25)
        self.c_list = []
        self.c1.Append_To(self.c_list)
        self.c2.Append_To(self.c_list)
        self.c3.Append_To(self.c_list)

    def Test_In_Range(self):
        self.assertTrue(self.c1.In_Range())

    def Test_R_Square(self):
        R_true = 3 * (0.5**4)
        R_test = Total_R_Square(self.c_list)
        self.assertEqual(R_true, R_test)

    def Test_Distance(self):
        D_true = 0
        D_test = self.c1.Distance(self.c2)
        self.assertEqual(D_true, D_test)

    def Test_Max_R(self):
        R_true = 0.5
        R_test = Max_Radius(self.c4, self.c_list)
        self.assertEqual(R_true, R_test)


if __name__ == "__main__":
    unittest.main(verbosity=2)
