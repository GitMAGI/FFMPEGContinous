import time
import sys
import os
import subprocess
import socket

def main():
    print("Starting ...")
    start_time = time.time()
    
    adb_push()

    elapsed_time = time.time() - start_time
    print("Completed in %s" % elapsed_time_string(elapsed_time))


def elapsed_time_string(elapsed_time):
    millis = int(round(elapsed_time * 1000))
    return time.strftime("%H:%M:%S", time.gmtime(elapsed_time)) + str(".%03d" % millis)


def get_args():
    device_name = ''
    return

def adb_push():
    return


if __name__ == "__main__":
    main()