import time
import sys
import os
import io
import subprocess
import asyncio

def main():
    print("Starting ...")
    start_time = time.time()

    for arg in sys.argv[1:]:
        pass

    try:
        if sys.platform == 'win32':
            loop = asyncio.ProactorEventLoop()
            asyncio.set_event_loop(loop)
        else:
            loop = asyncio.get_event_loop()
        loop.run_until_complete(job05())
    except KeyboardInterrupt:
        print("Received exit signal!")
    finally:
        if loop:
            loop.close()

    elapsed_time = time.time() - start_time
    print("Completed in %s" % elapsed_time_string(elapsed_time))

def elapsed_time_string(elapsed_time):
    millis = int(round(elapsed_time * 1000)) % 1000
    return time.strftime("%H:%M:%S", time.gmtime(elapsed_time)) + str(".%03d" % millis)

async def job05():
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

    time.sleep(0.5)

    # Initiate the FFMPEG Decode Process
    device_height = 1920
    device_width = 1080
    scaling_factor = 0.1
    s_height = int(device_height * scaling_factor)
    s_width = int(device_width * scaling_factor)  
    rgb_size_frame = s_height * s_width * 3

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
    cmd_string = " ".join(cmd)
    print("Executing command: %s" % cmd_string)
    decode_process = await asyncio.create_subprocess_shell(cmd = cmd_string, stdin = asyncio.subprocess.PIPE, stdout = asyncio.subprocess.PIPE)

    fin = decode_process.stdin
    fout = decode_process.stdout

    slice_size = 1024
    read_timeout = 0.0001

    output_data = b''
    max_timeouts = 50000
    timeout_counter = 0
    overall_counter = 0
    while True:
        in_data = input_stream.read(slice_size)
        if in_data:
            #print("Read data from Input Stream. Slice Size %d B" % len(in_data))
            fin.write(in_data)
            #print("Written data to STDIN of the process. Data Size %d B" % len(in_data))
        
        time.sleep(0)

        try:
            output_data_slice = await asyncio.wait_for(fout.readline(), read_timeout)            
            #print("Read data from STDOUT of the process: %d B" % len(output_data_slice))
            output_data += output_data_slice
        except asyncio.TimeoutError:
            timeout_counter += 1
            #if timeout_counter > max_timeouts:
            #    break
        finally:
            overall_counter += 1

    time.sleep(0.5)
    
    print("Overall Counter %d. Timeout Counter %d" % (overall_counter, timeout_counter))
    print("Gathered outpt of size %d B" % len(output_data))

    write_output = False
    # OUTPUT POST WRITING - BEGIN
    if write_output:
        output_path = 'output'        
        if output_data is not None and len(output_data) > 0:
            output_filename = 'data' + '_' + time.strftime("%Y%m%d-%H%M%S") + '.rgb24'
            output_fh = open(os.path.join(output_path, output_filename), 'ab')
            output_fh.write(output_data)
            output_fh.close()
            print("File %s successfully written!" % os.path.join(output_path, output_filename))
    # OUTPUT POST WRITING - END

    return await decode_process.wait()  

if __name__ == "__main__":
    main()