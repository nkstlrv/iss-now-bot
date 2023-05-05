import datetime
import time


def unix_converter(timestamp):
    d_time = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return d_time


if __name__ == "__main__":

    print(unix_converter(time.time()))