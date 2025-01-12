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