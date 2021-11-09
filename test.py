from math import sqrt, isqrt
from decorators import function_timer

num = 21**2

@function_timer
def func_1(num):
    for n in range(100000000):
        n1 = sqrt(num)

@function_timer
def func_2(num):
    for n in range(100000000):
        n1 = isqrt(num)

func_2(num)
func_1(num)
