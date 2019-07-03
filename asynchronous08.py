import time
import sys
import subprocess
import os

def main():
    print("Starting ...")
    start_time = time.time()

    for arg in sys.argv[1:]:
        pass

    job08()

    elapsed_time = time.time() - start_time
    print("Completed in %s" % elapsed_time_string(elapsed_time))


def elapsed_time_string(elapsed_time):
    millis = int(round(elapsed_time * 1000))
    return time.strftime("%H:%M:%S", time.gmtime(elapsed_time)) + str(".%03d" % millis)


def job08():
    if len(sys.argv) < 5:
        sys.stderr.write("Not enough options specified. Execution aborted!\n")
        return
    
    #device_height = 1920
    #device_width = 1080
    #scaling_factor = 0.1
    #tcp_address = 'localhost'
    #tcp_port = 12332

    device_height = int(sys.argv[1])
    device_width = int(sys.argv[2])
    scaling_factor = float(sys.argv[3])
    tcp_address = sys.argv[4]
    tcp_port = int(sys.argv[5])  

    print("device_height: %d" % device_height)
    print("device_width: %d" % device_width)
    print("scaling_factor: %f" % scaling_factor)
    print("tcp_address: %s" % tcp_address)
    print("tcp_port: %d" % tcp_port)

    # Initiate the FFMPEG Decode Process
    s_height = int(device_height * scaling_factor)
    s_width = int(device_width * scaling_factor)  
    rgb_size_frame = s_height * s_width * 3    

    cmd = [
        'ffmpeg',        
        '-i', 'tcp://{}:{}'.format(tcp_address, tcp_port),
        '-c:v', 'rawvideo',
        '-f', 'rawvideo',
        '-an','-sn',               # we want to disable audio processing (there is no audio)
        '-pix_fmt', 'rgb24',
        '-s', '{}x{}'.format(s_height, s_width),
        'pipe:1'
    ]
    cmd_string = " ".join(cmd)
    print("Executing command: %s" % cmd_string)
    output_process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)

    frames = []
    output_data = b''
    while True:
        if len(output_data) >= rgb_size_frame:
            frame = output_data[0:rgb_size_frame]
            frames.append(frame)
            output_data = output_data[rgb_size_frame:len(output_data)]

        #print("In reading ...")
        frame = output_process.stdout.read(rgb_size_frame)

        if frame == '' and output_process.poll() is not None:
            break
        else:
            frames.append(frame)

        #print("Data Read. Size of %d B", len(frame))

        #Only for debug
        if(len(frames) > 200):
            break
    
    print("Total Frames %d" % len(frames))

    #Only fro debug
    write_output = True
    # OUTPUT POST WRITING - BEGIN
    if write_output:
        output_path = 'output'
        
        if frames is not None and len(frames) > 0:
            output_filename = 'data' + '_' + time.strftime("%Y%m%d-%H%M%S") + '.rgb24'
            output_fh = open(os.path.join(output_path, output_filename), 'ab')
            for frame in frames:
                output_fh.write(frame)
            output_fh.close()
            print("File %s successfully written!" % os.path.join(output_path, output_filename))
    # OUTPUT POST WRITING - END

    return output_process.poll()
    

if __name__ == "__main__":
    main()