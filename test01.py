import subprocess

print("Starting ...")

device_screen_height = 1920
device_screen_width = 1080
scaling_factor = 0.1

ffmpeg_cmd = [
    'ffmpeg',
    '-c:v', 'h264',
    '-f', 'h264',
    '-i', 'pipe:0',
    '-c:v', 'rawvideo', 
    '-f', 'rawvideo', 
    '-pix_fmt', 
    'yuv420p', 
    '-s', '{}x{}'.format(int(device_screen_width*scaling_factor), int(device_screen_height*scaling_factor)),
    'pipe:1'
]

ffmpeg_proc = subprocess.Popen(
    ffmpeg_cmd,
    stdout = subprocess.PIPE,
    stdin = subprocess.PIPE
) 

print("Completed")