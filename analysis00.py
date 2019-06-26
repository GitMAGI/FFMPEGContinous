import os

device_height = 1920
device_width = 1080
scaling_factor = 0.1
s_height = int(device_height * scaling_factor)
s_width = int(device_width * scaling_factor)
rgb_frame_size = s_width * s_height * 3

def AnalizeData(input_data, rgb_frame_size, header):
    print("###### %s - BEGIN ######" % header)
    data_len = len(input_data)
    frames_number = data_len / rgb_frame_size
    print("Data Type: %s" % "RGB 24 bit")
    print("Width: %d" % s_width)
    print("Height: %d" % s_height)
    print("Frame Size: %d Bytes" % rgb_frame_size)
    print("Input Data Size: %d" % data_len)
    print("Number of Frames: %f" % frames_number)
    frames = []
    for i in range(1, data_len, rgb_frame_size):
        start = i
        stop = min([data_len, i+rgb_frame_size])
        frame = input_data[start:stop]
        frames.append(frame)
    print("###### %s - END ######" % header)
    print("")
    return frames

print("Starting ...")

input_path = 'output'
input_ffmpeg_raw = 'dataRaw_20190626-103846.rgb24'
input_my_processing = 'data_20190626-103646.rgb24'
input_my_processing_ba = 'dataBA_20190626-103646.rgb24'

input_fh = open(os.path.join(input_path, input_ffmpeg_raw), 'rb')
input_data_ffmpeg_raw = input_fh.read()
input_fh.close()

input_fh = open(os.path.join(input_path, input_my_processing), 'rb')
input_data_my_processing = input_fh.read()
input_fh.close()

input_fh = open(os.path.join(input_path, input_my_processing_ba), 'rb')
input_data_my_processing_ba = input_fh.read()
input_fh.close()

frames_my_processing = AnalizeData(input_data_my_processing, rgb_frame_size, "MY PROCESSING BYTES")
frames_my_processing_ba = AnalizeData(input_data_my_processing_ba, rgb_frame_size, "MY PROCESSING BYTES ARRAY")
frames_ffmpeg_raw = AnalizeData(input_data_ffmpeg_raw, rgb_frame_size, "FFMPEG RAW")

#print("%d" % len(frames_my_processing))
#print("%d" % len(frames_my_processing_ba))
#print("%d" % len(frames_ffmpeg_raw))

#print("%s" % type(frames_my_processing[1]))
#print("%s" % type(frames_my_processing_ba[1]))
#print("%s" % type(frames_ffmpeg_raw[1]))

print("Completed")