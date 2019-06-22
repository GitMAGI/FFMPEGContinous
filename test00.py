import time
import sys
import os
import subprocess

print("Starting ...")

process = subprocess.Popen(
    [
        'ffmpeg',
        '-f', 'h264',
        '-c:v', 'h264',
        '-i', '-',           
        '-pix_fmt', 'yuv420p', 
        '-f', 'rawvideo',
        '-an','-sn',               # we want to disable audio processing (there is no audio)
        '-'
    ],
    stdin = subprocess.PIPE, 
    stdout = subprocess.PIPE
)
print("Process Created")

input_path = 'input'
video_filename = 'video.mp4'

input_fh = open(os.path.join(input_path, video_filename), 'rb')
input_data = input_fh.read()
input_fh.close

print("Starting Processing ...")

slice_size = 1024
for i in range(1, len(input_data), slice_size):
    start = i
    stop = min([i + slice_size, len(input_data)])
    slice_data = input_data[start:stop]
    #print(start)
    #print(stop)
    #print(slice_data)

    process.stdin.write(slice_data)
    while process.poll() is None:
        print("I'm reading")
        data_size = 1
        output = process.stdout.read(data_size)
        print(output)

print("Completed")