import time
import sys
import os
import io
import ffmpy3
import subprocess

def main():
    print("Starting ...")
    start_time = time.time()

    for arg in sys.argv[1:]:
        pass

    job05()

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

    ff = ffmpy3.FFmpeg(
        inputs={'pipe:0': '-c:v h264 -f h264'},
        outputs={'pipe:1': '-c:v rawvideo -f rawvideo -an -sn -pix_fmt rgb24 -s {}x{}'.format(s_height, s_width)}
    )

    stdout, stderr = ff.run(input_data = input_stream.read(), stdout = subprocess.PIPE)
    #print(type(stdout))
    
    rgb_frames = []
    for i in range(0, len(stdout), rgb_size_frame):
        rgb_frame = stdout[i:rgb_size_frame]
        rgb_frames.append(rgb_frame)

    print("Total Frames %d" % len(rgb_frames))

if __name__ == "__main__":
    main()