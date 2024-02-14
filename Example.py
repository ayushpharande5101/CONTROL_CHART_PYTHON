byte_data = b'\x05\x00\x00\x00gfsgs\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

# Locate the start and end positions of the string within the byte data
start_index = 4  # Skip the first 4 bytes
end_index = byte_data.index(b'\x00', start_index)  # Find the position of the first null byte after the start index

# Extract the string from the byte data
string_data = byte_data[start_index:end_index].decode('utf-8')

print(string_data)
