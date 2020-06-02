import random

def selfsort(list):
    '''
    for i in range(len(list)):
        for j in range(len(list)):
            if list[i] < list[j]:
                list[i], list[j] = list[j], list[i]
    '''
    list.sort()
    print(list)
    #for i in range(len(list), 0, -1):
    #    print(list[:i])

def rand_test(listnum):
    a = random.sample(range(0, (2**31)-1), listnum)
    print(a)
    selfsort(a)

if __name__ == '__main__':
    listnum = 10000
    rand_test(listnum)