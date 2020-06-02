import random
from functools import reduce

from pythonTest.timeit import timeit

def mult(x, y):
    return x*y

def Factorials(n):
    if n==0 or n==1:
        return 1
    else:
        return n*Factorials(n-1)

def Factorials_mult(f_list):
    return reduce(lambda x,y:x*y, f_list)

def Factorials_lambda(f_list):
    return reduce(lambda x,y:x*y, f_list)

# -*- coding: utf-8 -*-
def turning(s,*arg):
    #注意不要写成字符串形式了
    print(s % arg)

if __name__ == '__main__':
    f_list = list(range(1, 10))

    timeit(Factorials(9))
    timeit(Factorials_mult(f_list))
    timeit(Factorials_lambda(f_list))

    turning('%d and %d', 7, 9)

