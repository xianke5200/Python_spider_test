'''
如下函数中带装饰器的运行时间比不带装饰器的运行时间要慢一个数量级
但是该程序样例执行的功能比较简单，所以不具备广泛的参考意义
'''
import time
def timeit(func):
    #def wrapper(a, b):
    stime = time.clock()
    result = func
    etime = time.clock()
    print(result, etime-stime)
    #return wrapper

#@timeit
def test(a, b):
    return a-b

if __name__ == '__main__':
    timeit(test(2,1))
    #test(2, 1)