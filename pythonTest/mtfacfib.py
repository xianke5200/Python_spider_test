#!/usr/bin/env python

from time import sleep, ctime

from pythonTest.myThread import MyThread


def fib(x):
    sleep(0.005)
    if x < 2: return 1
    return (fib(x-2)+fib(x-1))

def fac(x):
    sleep(0.1)
    if x < 2: return 1
    return (x*fac(x-1))

def sum(x):
    sleep(0.1)
    if x < 2: return 1
    return (x+sum(x-1))

funcs = [fib, fac, sum]
n = 12

def main():
    nfunc = range(len(funcs))

    print("*** SINGLE THREAD")
    for i in nfunc:
        print('starting', funcs[i].__name__, 'at:', ctime())
        funcs[i](n)
        print(funcs[i].__name__, 'finished at:', ctime())

    print('\n*** MULTIPLE THREADS')
    threads = []
    for i in nfunc:
        t = MyThread(funcs[i], (n,), funcs[i].__name__)
        threads.append(t)

    for i in nfunc:
        threads[i].start()

    for i in nfunc:
        threads[i].join()
        print(threads[i].getResult())

        print("all DONE")

if __name__ == '__main__':
    main()