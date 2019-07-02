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

    job03()

    elapsed_time = time.time() - start_time
    print("Completed in %s" % elapsed_time_string(elapsed_time))


def elapsed_time_string(elapsed_time):
    millis = int(round(elapsed_time * 1000)) % 1000
    return time.strftime("%H:%M:%S", time.gmtime(elapsed_time)) + str(".%03d" % millis)


def job03():
    input_path = 'input'
    input_filename = 'video.mp4'
    input_fullfilename = os.path.join(input_path, input_filename)
    cmd = [
        'ffmpeg', '-i', input_fullfilename, '-c:v', 'h264', '-f', 'h264', 'pipe:1'
    ]
    input_process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
    [input_data, input_err] = input_process.communicate(input = input_process)
    if input_err:
        sys.stderr.write(input_err + "\n")
        return
    print("Got %d Bytes of data" % len(input_data))

    # Simulate a stream buffer
    input_stream = io.BytesIO(input_data)

    # Initiate the FFMPEG Decode Process
    device_height = 1920
    device_width = 1080
    scaling_factor = 0.1
    s_height = int(device_height * scaling_factor)
    s_width = int(device_width * scaling_factor)
    cmd = [
        'ffmpeg',
        '-c:v', 'h264',
        '-f', 'h264',
        '-i', 'pipe:0',
        '-c:v', 'rawvideo',
        '-f', 'rawvideo',
        '-an','-sn',               # we want to disable audio processing (there is no audio)
        '-pix_fmt', 'rgb24',
        '-s', '{}x{}'.format(s_height, s_width),
        'pipe:1'
    ]
    decode_process = subprocess.Popen(cmd, shell = False, stdin = subprocess.PIPE, stdout = subprocess.PIPE)
    decode_input_stream = decode_process.stdin
    decode_output_stream = decode_process.stdout

    time.sleep(2)

    # Start write to stdin of the Process
    initial_slice_size = 1024
    slice_size = initial_slice_size  
    chunk_size = s_height * s_width * 3
    bytes_counter = 0
    while True:  
        try:  
            to_write_data = read_stream(input_stream, slice_size)
            if(to_write_data is None or len(to_write_data) == 0):
                break

            len_written_data = write_stream(decode_input_stream, to_write_data)
            if(len(to_write_data) != len_written_data):
                raise Exception("Data Sent Size is different from Data Written Size")
            
            bytes_counter += len_written_data
            #The following IS a fu**ing bloody BLOCKING call!!!!!
            #decoded_data = read_stream(decode_output_stream, chunk_size)

            #print("Written %d bytes" % len_written_data)
            print("%d of %d Bytes with Slice Size of %d" % (bytes_counter, len(input_data), slice_size))

            # Reset slice_size
            if slice_size > initial_slice_size:
                slice_size = initial_slice_size
        except Exception as e:
            slice_size *= 2
            print(str(e))
            print("Current Slice Size %d Bytes" % slice_size)            


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
    print("Written %d Bytes in %s" % (len(data), elapsed_time_string(elapsed_time)))
    return len(data)


if __name__ == "__main__":
    main()