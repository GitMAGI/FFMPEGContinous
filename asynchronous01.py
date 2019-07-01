import time
import sys
import subprocess

def main():
    print("Starting ...")
    start_time = time.time()

    for arg in sys.argv[1:]:
        pass

    #job00()
    job01()

    elapsed_time = time.time() - start_time
    print("Completed in %s" % elapsed_time_string(elapsed_time))


def elapsed_time_string(elapsed_time):
    millis = int(round(elapsed_time * 1000)) % 1000
    return time.strftime("%H:%M:%S", time.gmtime(elapsed_time)) + str(".%03d" % millis)


def job00():
    fin = sys.stdin
    fout = sys.stdout

    data = read_stream(fin, 4)
    print("Got '%s'" % data)
    len_data = write_stream(fout, data)
    #time.sleep(1.234)


def job01():
    cmd = [
        "ping",
        "8.8.8.8",
        "-t"
    ]
    process = subprocess.Popen(cmd, stdin = subprocess.PIPE, stdout = subprocess.PIPE)
    fout = process.stdout

    for i in range(1, 10, 1):
        data = read_stream(fout)
        print(data)


def read_stream(stream, length = 0):
    print("Starting %s ..." % "read_stream")
    start_time = time.time()

    if stream is None:
        raise TypeError("Input Stream is None!")

    data = stream.readline() if length == 0 else stream.read(length)

    elapsed_time = time.time() - start_time
    print("Read %d Bytes in %s" % (len(data), elapsed_time_string(elapsed_time)))
    return data


def write_stream(stream, data):
    print("Starting %s ..." % "write_stream")
    start_time = time.time()

    if stream is None:
        raise TypeError("Output Stream is None!")

    if data is None:
        return 0

    stream.write(data)

    elapsed_time = time.time() - start_time
    print("Write %d Bytes in %s" % (len(data), elapsed_time_string(elapsed_time)))
    return len(data)


if __name__ == "__main__":
    main()