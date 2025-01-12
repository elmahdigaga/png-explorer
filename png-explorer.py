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
    hexData = f.read().hex()

print(hexData)

def iterator(current, start, stop, nb_bytes, data):
    start = current
    stop = current + (nb_bytes * 2)
    current = stop
    return data[start:stop]