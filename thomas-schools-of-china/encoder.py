from PIL import Image
import struct
import random

INPUT_IMAGE = "duck.png"
OUTPUT_FILE = "chall.tsc"
MAGIC = b"TSCF"
VERSION = 1

#flag!
hex_chunks = [
    "746a63","74667b","63306e","677234","74735f","755f73","306c76","33645f",
    "6d795f","663173","745f43","54465f","636861","6c6c21","5f6274","775f31",
    "5f6c31","6b655f","623172","64737d"
]
payload = [bytes.fromhex(h) for h in hex_chunks]

img = Image.open(INPUT_IMAGE).convert("RGB")
width, height = img.size
pixels = list(img.getdata())
n = len(pixels)

#range of pixels to encode
box_size = 17
cx, cy = width // 2, height // 2
x0 = cx - box_size // 2
y0 = cy - box_size // 2 + 8

valid_positions = []
for y in range(y0, y0 + box_size):
    for x in range(x0, x0 + box_size):
        if 0 <= x < width and 0 <= y < height:
            valid_positions.append(y * width + x)

seed = 1337
rng = random.Random(seed)

#shuffle to get random
rng.shuffle(valid_positions)

spread_positions = valid_positions[:len(payload) * 2]
payload_positions = spread_positions[::2][:len(payload)]

payload_positions.sort()

# map in order
payload_map = dict(zip(payload_positions, payload))

#write file!
with open(OUTPUT_FILE, "wb") as f:
    # HEADER
    f.write(MAGIC)
    f.write(struct.pack("B", VERSION))
    f.write(struct.pack(">I", width))
    f.write(struct.pack(">I", height))
    f.write(struct.pack(">I", seed))

    # pixel stream
    for i in range(n):
        if i in payload_map:
            r, g, b = payload_map[i]
        else:
            r, g, b = pixels[i]
        f.write(bytes((r, g, b)))
        f.write(b"\x00")

print(f"Saved {OUTPUT_FILE}")
print(f"Payload hidden in center {box_size}x{box_size}")
print(f"Pixels modified: {len(payload)}")