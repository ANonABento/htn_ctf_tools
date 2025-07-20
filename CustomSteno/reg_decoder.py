import sys
import os
from PIL import Image

def decode_rgb_lsb(image_path):
    image = Image.open(image_path).convert("RGB")
    pixels = image.load()
    w, h = image.size

    bits = ""
    for y in range(h):
        for x in range(w):
            r, g, b = pixels[x, y]
            bits += str(r & 1)
            bits += str(g & 1)
            bits += str(b & 1)

    chars = []
    for i in range(0, len(bits) - 7, 8):
        byte = bits[i:i+8]
        try:
            ch = chr(int(byte, 2))
            if ch == 'þ':  # End sentinel
                break
            chars.append(ch)
        except ValueError:
            continue

    return ''.join(chars)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python decode_rgb_lsb.py <imagefile>")
        sys.exit(1)

    img_path = sys.argv[1]

    if not os.path.isfile(img_path):
        print(f"File not found: {img_path}")
        sys.exit(1)

    message = decode_rgb_lsb(img_path)

    base_name = os.path.splitext(os.path.basename(img_path))[0]
    output_file = f"{base_name}_decoded.txt"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(message)

    print(f"✅ Message written to {output_file}")
    print("🔍 Message preview:", message[:100])
