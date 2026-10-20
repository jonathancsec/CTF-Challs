from PIL import Image
import struct

INPUT_FILE = "chall.tsc"
OUTPUT_IMAGE = "reconstructed.png"

with open(INPUT_FILE, "rb") as f:

    #header
    magic = f.read(4)
    if magic != b"TSCF":
        raise ValueError("Not a valid .tsc file")

    version = struct.unpack("B", f.read(1))[0]
    width = struct.unpack(">I", f.read(4))[0]
    height = struct.unpack(">I", f.read(4))[0]
    seed = struct.unpack(">I", f.read(4))[0]

    #pixel data
    pixels = []

    while True:
        rgb = f.read(3)
        if len(rgb) < 3:
            break

        pixels.append(tuple(rgb))

        sep = f.read(1)
        if not sep:
            break

expected = width * height
pixels = pixels[:expected]

# rebuild
img = Image.new("RGB", (width, height))
img.putdata(pixels)
img.save(OUTPUT_IMAGE)

print(f"Reconstructed image saved as {OUTPUT_IMAGE}")
print(f"Size: {width}x{height}")
print(f"Pixels read: {len(pixels)}")


#result is reconstructed.png