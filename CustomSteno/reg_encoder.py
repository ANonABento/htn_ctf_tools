import sys
import os
from PIL import Image

def encode_rgb_lsb(image_path, output_path, message):
    # Add end sentinel
    message += 'þ'
    bits = ''.join(f"{ord(c):08b}" for c in message)

    image = Image.open(image_path).convert("RGB")
    pixels = image.load()
    w, h = image.size

    bit_index = 0
    max_bits = len(bits)

    for y in range(h):
        for x in range(w):
            if bit_index >= max_bits:
                break

            r, g, b = pixels[x, y]

            # Modify R
            if bit_index < max_bits:
                r = (r & ~1) | int(bits[bit_index])
                bit_index += 1
            # Modify G
            if bit_index < max_bits:
                g = (g & ~1) | int(bits[bit_index])
                bit_index += 1
            # Modify B
            if bit_index < max_bits:
                b = (b & ~1) | int(bits[bit_index])
                bit_index += 1

            pixels[x, y] = (r, g, b)

    if bit_index < max_bits:
        raise ValueError("Image not large enough to encode the full message.")

    image.save(output_path)
    print(f"✅ Message encoded and saved to {output_path}")
    print(f"💡 Total bits written: {bit_index} / {max_bits}")

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python encode_rgb_lsb.py <input_image> <output_image> <message>")
        sys.exit(1)

    input_img = sys.argv[1]
    output_img = sys.argv[2]
    message = sys.argv[3]

    if not os.path.isfile(input_img):
        print(f"File not found: {input_img}")
        sys.exit(1)

    encode_rgb_lsb(input_img, output_img, message)


# To use: python3 reg_encoder.py assets/input.png assets/output.png "secret message here"