import time
import sys
import os
import io
import subprocess

def main():
    print("Starting ...")
    start_time = time.time()

    for arg in sys.argv[1:]:
        pass

    #job00()
    #job01()
    job02()

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
    process = subprocess.Popen(cmd, stdout = subprocess.PIPE)
    fout = process.stdout

    for i in range(1, 10, 1):
        data = read_stream(fout)
        print(data)


def job02():
    input_path = 'input'
    input_filename = 'video.mp4'
    input_fullfilename = os.path.join(input_path, input_filename)
    cmd = [
        'ffmpeg', '-i', input_fullfilename, '-c:v', 'h264', '-f', 'h264', 'pipe:1'
    ]
    input_process = subprocess.Popen(cmd, stdout = subprocess.PIPE)
    [input_data, input_err] = input_process.communicate(input = input_process)
    if input_err:
        sys.stderr.write(input_err + "\n")
        return
    print("Got %d Bytes of data" % len(input_data))

    # Simulate a stream buffer
    input_stream = io.BytesIO(input_data)

    # Start write to stdin of the Process
    chunk_size = 1024
    while True:
        input_chunk = read_stream(input_stream, chunk_size)
        if input_chunk == '' or input_chunk == b'' or input_chunk == None:
            break
        #print(input_chunk)




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