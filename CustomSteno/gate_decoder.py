import sys
import os
from PIL import Image

def gated_logic(color):
    # Extract bits from blue (MSB first)
    bits = [(color >> i) & 1 for i in reversed(range(8))]

    t1 = ((bits[1] & bits[2]) | bits[4]) & bits[3]
    t2 = (bits[6] ^ bits[7]) & bits[5]
    t3 = ((~bits[0]) & 1) & t1
    t4 = t1 | t2
    t5 = t1 | t4
    t6 = t3 & t5

    return t6

def decode_message(image_path):
    image = Image.open(image_path).convert("RGB")
    pixels = image.load()
    w, h = image.size

    bits = ""
    for y in range(h):
        for x in range(w):
            r, g, b = pixels[x, y]
            bits += str(gated_logic(r))                 # Red channel LSB
            bits += str(gated_logic(g))                 # Green channel LSB
            bits += str(gated_logic(b)) # Custom blue logic bit

    # Convert bits to characters
    chars = []
    for i in range(0, len(bits) - 7, 8):  # process full bytes only
        byte = bits[i:i+8]
        try:
            ch = chr(int(byte, 2))
            if ch == '\0':
                break
            chars.append(ch)
        except ValueError:
            continue  # skip bad bytes

    message = ''.join(chars)
    return message

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python lsb_decode.py <imagefile>")
        sys.exit(1)

    img_path = sys.argv[1]
    if not os.path.isfile(img_path):
        print(f"File not found: {img_path}")
        sys.exit(1)

    message = decode_message(img_path)

    base_name = os.path.splitext(os.path.basename(img_path))[0]
    output_file = f"{base_name}_decoded.txt"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(message)

    print(f"✅ Message written to {output_file}")
    print("🔍 Message preview:", message[:100])
