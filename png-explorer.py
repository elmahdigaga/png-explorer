image_path = "./dice.png"

with open(image_path, "rb") as f:
    hexData = f.read().hex()

def iterator(current, start, stop, nb_bytes, data):
    start = current
    stop = current + (nb_bytes * 2)
    current = stop
    return data[start:stop]