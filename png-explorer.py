import os
import sys
import math
from collections import Counter


class Chunk:
    def __init__(self, type, data_length, data, crc):
        self.type = type
        self.data_length = data_length
        self.data = data
        self.crc = crc
        self.crc_ref = self._reflect_crc(crc)
        self.entropy = 0 if (type == "IEND") else self._calculate_entropy(data)

    @staticmethod
    def _reflect_crc(crc, width = 32):
        reflected = 0
        crc_value = int(crc, 16)
        for bit in range(width):
            reflected = (reflected << 1) | (crc_value & 1)
            crc_value >>= 1
        return reflected
    
    @staticmethod
    def _calculate_entropy(data):
        if not data:
            return 0
        counter = Counter(data)
        total = len(data)
        # Shannon's formula for calculating the entropy
        return -sum((count / total) * math.log2(count / total) for count in counter.values())
    
    def __str__(self):
        return f"{self.type}, {self.data_length}, {self.crc}, {self.crc_ref}, {self.entropy:.2f}"


def iterator(pointer, nb_bytes, data):
    start = pointer
    stop = pointer + (nb_bytes * 2)
    pointer = stop
    return data[start:stop], pointer

def extract_chunks(data):
    chunks = []
    pointer = 16
    while True:
        # Get the chunk data length (size: 4 bytes)
        data_length_hex, pointer = iterator(pointer, 4, data)
        data_length = int(data_length_hex, 16)

        # Get the chunk type (size: 4 bytes)
        type_hex, pointer = iterator(pointer, 4, data)
        type = bytes.fromhex(type_hex).decode()

        # Get the chunk data (size: indicated by the chunk data length)
        data_hex, pointer = iterator(pointer, data_length, data)

        # Get the chunk CRC (size: 4 bytes)
        crc_hex, pointer = iterator(pointer, 4, data)

        chunk = Chunk(type, data_length, data_hex, crc_hex)
        chunks.append(chunk)

        # If END OF FILE detected, break the loop
        if type == "IEND":
            break
    return chunks


def main():
    if len(sys.argv) == 2:
        png_path = sys.argv[1]
    else:
        png_path = input("Enter the png file path : ")

    if not os.path.isfile(png_path):
        print("Error: File not found")
        exit(1)

    try:
        with open(png_path, "rb") as file:
            hex_data = file.read().hex()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Get the signature (size: 8 bytes)
    pointer = 0
    signature_hex, pointer = iterator(pointer, 8, hex_data)
    if signature_hex != "89504e470d0a1a0a":
        print("Error: Invalid PNG signature")
        sys.exit(1)

    chunks = extract_chunks(hex_data)
    print("type, size, CRC, CRC_ref, entropy")
    for chunk in chunks:
        print(chunk)

if __name__ == "__main__":
    main()