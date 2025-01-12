import os
import sys

if sys.argv.count == 2:
    png_path = sys.argv[1]
else:
    png_path = input("Enter the png file path : ")

if not os.path.isfile(png_path):
    print("Error: File not found")
    exit(1)

with open(png_path, "rb") as f:
    hex_data = f.read().hex()

def iterator(current, nb_bytes, data):
    start = current
    stop = current + (nb_bytes * 2)
    current = stop
    return data[start:stop], current


current = 0
# Get the signature (size: 8 bytes)
signature_hex, current = iterator(current, 8, hex_data)
if not signature_hex == "89504e470d0a1a0a":
    print("Error: Invalid signature")
    exit(1)
print("Signature : ", signature_hex)


### CHUNK: 4 bytes: length | 4 bytes: Type | x bytes: Data | 4 bytes: CRC

# Get the chunk data length (size: 4 bytes)
data_length_hex, current = iterator(current, 4, hex_data)
data_length = int(data_length_hex, 16)
print("Chunk data length : ", data_length)

# Get the chunk type (size: 4 bytes)
type_hex, current = iterator(current, 4, hex_data)
type = bytes.fromhex(type_hex).decode()
print("Chunk type : ", type)

# skip the chunk data (size: indicated by the chunk data length)
data_hex, current = iterator(current, data_length, hex_data)

# Get the chunk CRC (size: 4 bytes)
crc_hex, current = iterator(current, 4, hex_data)
print("Chunk CRC : 0x" + crc_hex)

def reflect_crc(crc, width = 32):
    reflected = 0
    crc_value = int(crc, 16)
    for bit in range(width):
        reflected = (reflected << 1) | (crc_value & 1)
        crc_value >>= 1
    return reflected

# Get the reflected CRC
crc_ref_hex = hex(reflect_crc(crc_hex))
print("Chunk's reflected CRC : " + crc_ref_hex)