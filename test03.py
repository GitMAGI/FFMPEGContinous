import io

print("Starting ...")

slice_size = 7
data_to_write = b'la maestra caga a rootoomia'

output_buffer = io.BytesIO()
print("Buffer Content %s. Buffer Length: %d B" % (output_buffer.getvalue(), output_buffer.getbuffer().nbytes))
print("Data To Write %s. Size %d B" %(data_to_write, len(data_to_write)))
output_buffer.write(data_to_write)
print("Buffer Content %s. Buffer Length: %d B" % (output_buffer.getvalue(), output_buffer.getbuffer().nbytes))
output_buffer.seek(0)
data_read = output_buffer.read(slice_size)
output_buffer.seek(slice_size)
output_buffer.truncate(slice_size)
print("Data Read %s. Size %d B" %(data_read, len(data_read)))
print("Buffer Content %s. Buffer Length: %d B" % (output_buffer.getvalue(), output_buffer.getbuffer().nbytes))

print("Completed")