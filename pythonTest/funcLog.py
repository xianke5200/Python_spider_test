

from time import time

def logged(when):
    def log(f, *args, **kargs):
        print("Called:\n"
              "function: %s\n"
              "args: %r\n"
              "kargs: %r" %(f, args, kargs))

    def pre_logged(f):
        def wrapped(*args, **kargs):
            log(f, *args, **kargs)
            return f(*args, **kargs)
        return wrapped

    def post_logged(f):
        def wrapped(*args, **kargs):
            now = time()
            try:
                return f(*args, **kargs)
            finally:
                log(f, *args, **kargs)
                print("time delta: %s" %(time()- now))
        return wrapped

    try:
        return {"pre": pre_logged,
                "post": post_logged}[when]
    except KeyError as e:
        raise ValueError(e, 'must be "pre" or "post"')

@logged("post")
def hello(name):
    print("hello", name)

hello("world!")
'''
j, k = 1, 2

def proc1():
    j, k = 3, 4
    print("proc1: j = %d, k = %d" %(j, k))
    k = 5

def proc2():
    j = 6
    proc1()
    print("proc2: j = %d, k = %d" % (j, k))

k = 7
proc1()
print("one: j = %d, k = %d" % (j, k))

j = 8
proc2()
print("two: j = %d, k = %d" % (j, k))
'''