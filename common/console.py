import time

ISOTIMEFORMAT = "%Y/%m/%d %X"


def log(state, message):
    now_time = time.strftime(ISOTIMEFORMAT, time.localtime())
    print("{0} [{1}] {2}".format( now_time, state, message))
