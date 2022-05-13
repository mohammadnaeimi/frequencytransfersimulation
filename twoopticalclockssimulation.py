from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import scipy as sp
from scipy.integrate import odeint
import random

# Initial definations
DeltaW_re = 300
n = 140
c = 2.9 * 10e8

delta0_ab = 0.6
eci = [random.uniform(-0.0000000002, 0.0000000003) for i in range(n)]
eti = [random.uniform(-0.0000000006, 0.0000000008) for i in range(n)]
delta0 = delta0_ab + eti[0] + eci[0]


# This function generates the ith random observations
def Delta(i):
    deltai = delta0_ab + 3.3 * 10e-15 * (i + eci[i]) + eti[i] + eci[0]
    return deltai


# collecting n numbers of random observations
t = [Delta(i) for i in range(n)]


def Sxy1(n):
    Sxy1 = 0
    for i in range(n):
        Sxy1 += (t[i] - delta0) * i
    return Sxy1
def Sxy2(n):
    Sxy2 = 0
    for i in range(n):
        Sxy2 += (t[i] - delta0)
    return (n + 1.0) / 2.0 * Sxy2


# The quantity of a^ and b^ in terms of the numbers of observations
def a_hat(n):
    return (Sxy1(n) - Sxy2(n)) / ((n * (n + 1) * (2 * n + 1)) / 6 - (n * (n + 1) ** 2) / 4)
def b_hat(n):
    res = 0
    for i in range(n):
        res += t[i] - delta0
    return (1.0 / n) * res - (1.0 / 2.0) * a_hat(n) * (n + 1)

# The standard deviation of data in terms of the numbers of observation
def delta_dev(n):
    factor = np.sqrt(n - 2)
    res = 0
    for i in range(n):
        res += (t[i] - delta0 - a_hat(n) * i - b_hat(n)) ** 2
    return (1.0 / factor) * np.sqrt(res)

# The standard deviation of a^:
def delta_a_hat_dev(n):
    return delta_dev(n) / np.sqrt((n * (n + 1) * (2 * n + 1)) / 6 - (n * (n + 1) ** 2) / 4)

def DeltaW(n):
    return a_hat(n) * (c ** 2)

def DeltaW_dev(n):
    return delta_a_hat_dev(n) * (c ** 2)

# This list collects the n observation of Deltaw from n = 3

Func1 = []
for j in range(3, n):
    Func1.append(DeltaW_re - DeltaW_dev(j))

Func2 = []
for i in range(3, n):
    Func2.append(DeltaW_re - DeltaW(i))
count = [i for i in range(3, n)]

def main1():
    plt.plot(count, Func2, label = 'Dw')
    plt.xlabel('time ~ 1 min')
    plt.ylabel('DW ~ 300 $/frac(m^2,s^2)$')
    plt.legend(loc= 'best')
    plt.show()


    plt.plot(count, Func1, label = 'Dw deviation')
    plt.xlabel('time ~ 1 min')
    plt.ylabel('DW ~ 300 $/frac(m^2,s^2)$')
    plt.show()

    plt.legend(loc= 'best')
    return

if __name__ == '__main__':
    main1()