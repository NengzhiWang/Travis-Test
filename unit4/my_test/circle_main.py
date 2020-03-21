# -*- coding: utf-8 -*-

import random

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize
'''
Author: WangNengzhi
'''
'''
主要内容

1. class circle
    对圆的类型封装

2. 方法一
    随机生成一个圆的圆心坐标。则按照和其他圆/限定的正方形相切为目标，计算可行的最大半径。直到填入的圆的数量达到要求。
    该方法不会调整圆心坐标的位置，因此求得的解不稳定而且严重偏小。

3. 方法二
    在方法一的基础上添加了scipy.minimize优化器，可以在局部范围内优化圆心坐标，使最大半径尽可能地大。
    圆心坐标初始值在四个象限内轮流生成。
    相对于方法一，可以获得更理想的结果。

4. 结果展示
    使用matplotlib进行绘图，展示结果
    方法一和方法二的结果实例见文件'Figure_1.png'和'Figure_2.png'，设置的m为20
'''
'''
问题

1. 方法二的优化器获得的是局部最优解，而非全局最优解。因此其结果仍然较小

'''


class circle:
    # center 圆心坐标，x + y * j
    # radius 半径
    # center = 0 + 0j
    x = 0
    y = 0
    radius = 0

    # 定义构造函数。输入变量为圆心坐标及半径
    def __init__(self, x, y, r):
        # self.center = complex(x, y)
        self.x = x
        self.y = y
        self.radius = abs(r)

    # 判断该圆是否处于限定范围内
    def In_Range(self):
        x = self.x
        y = self.y
        r = self.radius
        left = abs(x - r)
        right = abs(x + r)
        upper = abs(y + r)
        lower = abs(y - r)
        if max(left, right, upper, lower) > 1:
            return False
        else:
            return True

    # 以复数形式返回圆心坐标
    def Center(self):
        return complex(self.x, self.y)

    # 输出对象相关信息（圆心，半径）
    def print(self):
        x = self.x
        y = self.y
        r = self.radius
        print("Center\t(%f,%f) \t Radius\t%f" % (x, y, r))

    # 计算两个圆之间的距离
    def Distance(self, cir2):
        c_1 = self.Center()
        c_2 = cir2.Center()
        r_1 = self.radius
        r_2 = cir2.radius
        return abs(c_1 - c_2) - (r_1 + r_2)

    # 判断对象是否和另一个circle对象clr2有重叠部分
    def OverLap(self, cir2):
        # 计算两个圆间的距离，若小于0则有重叠部分
        Dist = self.Distance(cir2)
        if Dist < 0:
            return True
        elif Dist >= 0:
            return False

    # 将此对象添加到列表c_list中,返回是否添加成功
    # 需要判断该对象是否符合条件：和其他的圆无重叠部分
    def Append_To(self, c_list):
        # 判断该圆是否和列表中其他圆有重合部分
        if self.In_Range():
            Can_Attend = True
            if len(c_list) == 0:
                c_list.append(self)
                return True
            else:
                Can_Attend = not self.Center_Inside(c_list)
                for c in c_list:
                    Can_Attend = Can_Attend and not self.OverLap(c)

                if Can_Attend:
                    c_list.append(self)
                    return True
                else:
                    return False
        else:
            return False

    # 判断该圆的圆心是否在其他的圆内
    def Center_Inside(self, c_list):
        if len(c_list) == 0:
            return False
        else:
            Inside = False
            for c in c_list:
                c_1 = c.Center()
                r_1 = c.radius
                dis = abs(self.Center() - c_1)
                if dis <= r_1:
                    Inside += True
                    break
                else:
                    Inside += False

            return Inside


# 计算最大可行半径
def Max_Radius(cir, c_list):
    x = cir.x
    y = cir.y
    # 计算到边界的距离
    R_list = [1 - x, x + 1, 1 - y, y + 1]

    if not len(c_list) == 0:
        # 计算到其他各圆的距离
        for c in c_list:
            r = c.Distance(cir) + cir.radius
            R_list.append(r)
    # 从中取最小值，即最大可行半径
    return min(R_list)


# 计算c_list中所有圆的r^2之和
def Total_R_Square(c_list):
    R2 = 0
    for c in c_list:
        R2 += c.radius**2

    return R2


# 输出c_list中所有圆的信息
def Print_Circle(c_list):
    for c in c_list:
        c.print()


# 使用matplotlib进行绘图
def Plot_Circle(c_list):
    plt.figure()
    plt.axes().set_aspect('equal')
    plt.xlim([-1, 1])
    plt.ylim([-1, 1])
    theta = np.linspace(0, 2 * np.pi, 90)
    for c in c_list:
        x = c.x
        y = c.y
        r = c.radius
        plt.plot(x + r * np.cos(theta), y + r * np.sin(theta), 'r')

    plt.show()


# 计算在给定圆的数量的情况下，r^2最大时对应的圆的列表。方法一
def Random_Max_R_Square(circle_num):
    c_list = []
    # 向列表中添加新圆，直到总数符合要求
    while len(c_list) < circle_num:
        if len(c_list) == 0:
            # 第一个圆，强制设定为单位圆
            x = 0
            y = 0
            r = 1
        else:
            # 随机下一个圆的圆心坐标
            x = random.uniform(-1, 1)
            y = random.uniform(-1, 1)
            r = 0

        cir = circle(x, y, r)
        # 计算这个圆的最大半径，并添加进列表
        # 如果该圆不符合条件，则其无法被添加进列表
        cir.radius = Max_Radius(cir, c_list)
        cir.Append_To(c_list)
    return c_list


# 计算在给定圆的数量的情况下，r^2最大时对应的圆的列表。方法二
def Optimize_Max_R_Square(c_num):
    c_list = []
    # 向列表中添加新圆，直到总数符合要求
    while len(c_list) < c_num:
        cir_in_list = len(c_list)
        mod = (cir_in_list + 1) % 4
        if cir_in_list == 0:
            x = 0
            y = 0
            c = circle(x, y, 1)
            c.Append_To(c_list)
        else:
            # 在四个象限中轮流初始化
            if mod == 0:
                x = random.uniform(0, 1)
                y = random.uniform(0, 1)
            elif mod == 1:
                x = random.uniform(-1, 0)
                y = random.uniform(0, 1)
            elif mod == 2:
                x = random.uniform(-1, 0)
                y = random.uniform(-1, 0)
            elif mod == 3:
                x = random.uniform(0, 1)
                y = random.uniform(-1, 0)

            c = circle(x, y, 0)

            # 使用优化器，计算局部最优解
            Max_Circle = minimize(Center_Optimize(c_list), (c.x, c.y),
                                  method='SLSQP')
            # 将新圆更新为局部最优解，并添加进列表
            c.x = float(Max_Circle.x[0])
            c.y = float(Max_Circle.x[1])
            c.radius = Max_Radius(c, c_list)
            c.Append_To(c_list)

    return c_list


# 优化器，目标为使最大可能半径尽可能大
def Center_Optimize(c_list):
    return lambda x: 1 - Max_Radius(circle(x[0], x[1], 0), c_list)


if __name__ == "__main__":

    circle_num = 20
    # c_list = Random_Max_R_Square(circle_num)

    c_list = Optimize_Max_R_Square(circle_num)

    R2 = Total_R_Square(c_list)
    print("sum r^2的最大值为\t", R2)

    print("对应圆的参数")
    Print_Circle(c_list)

    Plot_Circle(c_list)
