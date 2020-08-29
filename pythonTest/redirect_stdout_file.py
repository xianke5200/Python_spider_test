import contextlib
import sys
import time

log_file = "log.txt"

@contextlib.contextmanager
def close_stdout():
    raw_stdout = sys.stdout
    file = open(log_file, 'a+')
    log_time = "{}年{}月{}日{}时{}分{}秒\r\n".format(
        time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday,
        time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec
    )
    file.write(log_time)
    sys.stdout = file

    yield

    sys.stdout = raw_stdout
    file.close()

def count_n():
    return 0

with close_stdout():
    count_n()
for i in iter(int, 1): #将int 替换为count_n，可实现相同效果
    print("{}".format(i))