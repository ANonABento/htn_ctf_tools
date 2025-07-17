import sys
import os
from PIL import Image

def int_to_bits(n):
    return format(n, '08b')

def decode_bit(value):
    return int_to_bits(value)[-1]  # Get LSB

def bin_to_text(bin_str):
    chars = [bin_str[i:i+8] for i in range(0, len(bin_str), 8)]
    text = ''
    for c in chars:
        if len(c) == 8:
            ch = chr(int(c, 2))
            if ch == '\0':  # Null terminator
                break
            text += ch
    return text

def decode_message(image_path):
    image = Image.open(image_path)
    image = image.convert("RGB")
    pixels = image.load()
    w, h = image.size

    bits = ""
    for y in range(h):
        for x in range(w):
            r, g, b = pixels[x, y]
            bits += str(r & 1)
            bits += str(g & 1)
            bits += str(b & 1)

    chars = [chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)]
    message = ''.join(chars)
    return message.split('\0', 1)[0]  # Stop at null byte


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
