import time

style = {
    'Success': 32, 'Error': 31
}
ISOTIMEFORMAT = "%Y/%m/%d %X"


def log(state, message):
    now_time = time.strftime(ISOTIMEFORMAT, time.localtime())
    color = 0
    if state in style:
        color = style[state]
    print("\033[{0}m{1} [{2}] {3}\033[0m".format(color, now_time, state, message))
