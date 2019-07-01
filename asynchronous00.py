import time
import sys

def main():
    print("Starting ...")
    start_time = time.time()

    for arg in sys.argv[1:]:
        pass

    #time.sleep(0.234)

    elapsed_time = time.time() - start_time
    print("Completed in %s" % elapsed_time_string(elapsed_time))


def elapsed_time_string(elapsed_time):
    millis = int(round(elapsed_time * 1000))
    return time.strftime("%H:%M:%S", time.gmtime(elapsed_time)) + str(".%03d" % millis)


if __name__ == "__main__":
    main()