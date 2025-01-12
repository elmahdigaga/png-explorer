import os
import sys
import math
from typing import Counter


if sys.argv.count == 2:
    png_path = sys.argv[1]
else:
    png_path = input("Enter the png file path : ")

if not os.path.isfile(png_path):
    print("Error: File not found")
    exit(1)

class Chunk:
    def __init__(self, type, data_length, data, crc):
        self.type = type
        self.data_length = data_length
        self.data = data
        self.crc = crc
        self.crc_ref = self.reflect_crc(crc)
        self.entropy = 0 if (type == "IEND") else self.calculate_entropy(data)

    def reflect_crc(self, crc, width = 32):
        reflected = 0
        crc_value = int(crc, 16)
        for bit in range(width):
            reflected = (reflected << 1) | (crc_value & 1)
            crc_value >>= 1
        return reflected
    
    def calculate_entropy(self, data):
        if not data:
            return 0
        
        counter = Counter(data)
        total = len(data)
        # Shannon's formula for calculating the entropy
        entropy = -sum((count / total) * math.log2(count / total) for count in counter.values())
        return entropy
    
    def __str__(self):
        return f"{self.type}, {self.data_length}, {self.crc}, {self.crc_ref}, {self.entropy}"


def iterator(current, nb_bytes, data):
    start = current
    stop = current + (nb_bytes * 2)
    current = stop
    return data[start:stop], current

def get_chunks(data, current):
    chunks = []
    while True:
        # Get the chunk data length (size: 4 bytes)
        data_length_hex, current = iterator(current, 4, data)
        data_length = int(data_length_hex, 16)

        # Get the chunk type (size: 4 bytes)
        type_hex, current = iterator(current, 4, hex_data)
        type = bytes.fromhex(type_hex).decode()

        # Get the chunk data (size: indicated by the chunk data length)
        data_hex, current = iterator(current, data_length, hex_data)

        # Get the chunk CRC (size: 4 bytes)
        crc_hex, current = iterator(current, 4, hex_data)

        chunk = Chunk(type, data_length, data_hex, crc_hex)
        chunks.append(chunk)

        # If END OF FILE detected, break the loop
        if type == "IEND":
            break
    return chunks


with open(png_path, "rb") as f:
    hex_data = f.read().hex()

current = 0
# Get the signature (size: 8 bytes)
signature_hex, current = iterator(current, 8, hex_data)
if not signature_hex == "89504e470d0a1a0a":
    print("Error: Invalid signature")
    exit(1)


chunks = get_chunks(hex_data, current)
print("type, size, CRC, CRC_ref, entropy")
for chunk in chunks:
    print(chunk)