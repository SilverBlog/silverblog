import time

style = {
    'black': 30, 'red': 31, 'green': 32, 'yellow': 33,
    'blue': 34, 'purple': 35, 'cyan': 36, 'white': 37,
    "none": 0
}
ISOTIMEFORMAT = "%Y/%m/%d %X"


def log(state, message, color="none"):
    now_time = time.strftime(ISOTIMEFORMAT, time.localtime())
    print("\033[{0}m".format(style[color]))
    print("{0} [{1}] {2}".format(now_time, state, message))
    print("\033[0m")
