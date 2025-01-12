image_path = "./dice.png"

with open(image_path, "rb") as f:
    hexData = f.read().hex()

print(hexData)