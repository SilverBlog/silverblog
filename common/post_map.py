import time


def build_time(time_s, system_info):
    return time.strftime(system_info["Time_Format"], time.localtime(time_s))
