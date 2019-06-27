import time
import sys
import os
import subprocess
import asyncio

print("Starting ...")

async def run_ffmpeg_read_async(slice_size, frames, timeout=None):
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
    process = asyncio.subprocess.create_subprocess_exec(    
        cmd,
        stdin = asyncio.subprocess.PIPE, 
        stdout = asyncio.subprocess.STDOUT
    )
    print("Command: '{}' started".format(" ".join(str(x) for x in cmd)))

    # read line (sequence of bytes ending with b'\n') asynchronously
    max_failures = 5
    failures = 0
    while True:
        try:
            frame = await asyncio.wait_for(process.stdout.read(slice_size), timeout)
            frames.add(frame)
            failures = 0
        except asyncio.TimeoutError:
            failures += 1
            pass
        else:
            if not frame: # EOF
                break
            elif failures <= max_failures: 
                continue # while some criterium is satisfied
        process.kill() # timeout or some criterium is not satisfied
        break
    return await process.wait() # wait for the child process to exit

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
rgb_frame_size = s_width * s_height * 3
unblocking_factor = 0.008

if sys.platform == "win32":
    loop = asyncio.ProactorEventLoop() # for subprocess' pipes on Windows
    asyncio.set_event_loop(loop)
else:
    loop = asyncio.get_event_loop()

frames = []
returncode = loop.run_until_complete(run_ffmpeg_read_async(rgb_frame_size, frames,  timeout = unblocking_factor))

loop.close()

print("Completed")