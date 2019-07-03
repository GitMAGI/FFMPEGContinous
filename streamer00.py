import time
import sys
import os
import subprocess
import socket

def main():
    print("Starting ...")
    start_time = time.time()
    
    streamer_job()

    elapsed_time = time.time() - start_time
    print("Completed in %s" % elapsed_time_string(elapsed_time))


def elapsed_time_string(elapsed_time):
    millis = int(round(elapsed_time * 1000))
    return time.strftime("%H:%M:%S", time.gmtime(elapsed_time)) + str(".%03d" % millis)

def streamer_job():
    if len(sys.argv) < 6:
        sys.stderr.write("Not enough options specified. Execution aborted!\n")
        return

    #input_path = 'input'
    #input_filename = 'video.mp4'
    #tcp_address = ''
    #tcp_port = 12332
    #slice_size = 1024
    #sleep_time = 0.0001

    input_path = sys.argv[1]
    input_filename = sys.argv[2]
    tcp_address = sys.argv[3]
    tcp_port = int(sys.argv[4])
    slice_size = int(sys.argv[5])
    sleep_time = float(sys.argv[6])

    print("input_path: %s" % input_path)
    print("input_filename: %s" % input_filename)
    print("tcp_address: %s" % tcp_address)
    print("tcp_port: %d" % tcp_port)
    print("slice_size: %d" % slice_size)
    print("sleep_time: %f" % sleep_time)

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

    time.sleep(1)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    s.bind((tcp_address, tcp_port))

    s.listen(1)
    
    while True:
        print('Server listening on %s:%d' % (tcp_address, tcp_port))

        conn, addr = s.accept()
        print('Client connection accepted ', addr)

        loop_counter = 1
        i = 0
        while True:
            try:
                start = i
                stop = min([i + slice_size, len(input_data)])                
                slice_data = input_data[start:stop] 
                #print('Slice Data size %d B' % len(slice_data))
                #print("Loop number %d - Start %d | Stop %d" % (loop_counter, start, stop))
                conn.send(slice_data)   
                time.sleep(sleep_time)
                i = stop 
                if(stop >= len(input_data)):
                    i = 0
                    loop_counter += 1
                    #print("%d of %d" %(stop, len(input_data)))
                    #print("Executing loop number %d ..." % loop_counter)
            except socket.error as e:                
                print('Client connection closed ', addr)
                break
            except Exception as e:
                sys.stderr.write(str(e) + "\n")
                break

        conn.close()    

if __name__ == "__main__":
    main()