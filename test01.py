import time
import sys
import os
from nbstreamreader import NonBlockingStreamReader as NBSR
import subprocess

print("Starting ...")

# INPUT PRE LOADING - BEGIN
input_path = 'input'
video_filename = 'video.mp4'
input_cmd = [ 'ffmpeg', '-i', os.path.join(input_path, video_filename), '-c:v', 'h264', '-f', 'h264', 'pipe:1' ]
input_fh = subprocess.Popen(input_cmd, stdout = subprocess.PIPE)
print("Command: '{}' started".format(" ".join(str(x) for x in input_cmd)))
[input_data, input_err] = input_fh.communicate(input = input_fh)
print("Got %d Bytes of data" % len(input_data))
# INPUT PRE LOADING - END

device_height = 1920
device_width = 1080

scaling_factor = 0.1
s_height = int(device_height * scaling_factor)
s_width = int(device_width * scaling_factor)

write_output = True
slice_size = 1024
rgb_frame_size = s_width * s_height * 3
unblocking_factor = 0.008

# C:\msys64\mingw64\bin\ffmpeg -i pipe:0 -c:v rawvideo -f rawvideo -an -pix_fmt rgb24 -s 192x108 pipe:1
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
process = subprocess.Popen(    
    cmd,
    stdin = subprocess.PIPE, 
    stdout = subprocess.PIPE
)
print("Command: '{}' started".format(" ".join(str(x) for x in cmd)))
fin = process.stdin
fout = NBSR(process.stdout, rgb_frame_size)

frames = []
frameBAs = []
for i in range(1, len(input_data), slice_size):
    start = i
    stop = min([i + slice_size, len(input_data)])
    slice_data = input_data[start:stop]

    #print(slice_data)
    fin.write(slice_data)

    try:
        decoded_frame = fout.read(unblocking_factor)
        #print(decoded_frame)
        if decoded_frame is not None:
            frames.append(decoded_frame)
            frameBAs.append(bytearray(decoded_frame))
    except Exception as e:
        #print(str(e))
        pass

    #print("%d of %d" % (stop, len(input_data)))

print("Collected %d frames" % len(frames))
print("Collected %d frames of byte arrays" % len(frames))

# OUTPUT POST WRITING - BEGIN
if write_output:
    output_path = 'output'
    
    if frameBAs is not None and len(frameBAs) > 0:
        output_filename = 'dataBA' + '_' + time.strftime("%Y%m%d-%H%M%S") + '.rgb24'
        output_fh = open(os.path.join(output_path, output_filename), 'ab')
        for frameBA in frameBAs:    
            output_fh.write(frameBA)
        output_fh.close()
    
    if frames is not None and len(frames) > 0:
        output_filename = 'data' + '_' + time.strftime("%Y%m%d-%H%M%S") + '.rgb24'
        output_fh = open(os.path.join(output_path, output_filename), 'ab')
        for frame in frames:
            output_fh.write(frame)
        output_fh.close()
# OUTPUT POST WRITING - END

print("Completed")