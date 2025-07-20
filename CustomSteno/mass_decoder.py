import sys
import os
from PIL import Image

def extract_bits(pixels, coords, channels=(0,1,2)):
    bits = ""
    for x, y in coords:
        r, g, b, _ = pixels[x, y]
        values = [r, g, b]
        for i in channels:
            bits += str(values[i] & 1)
    return bits

def bits_to_string(bits):
    chars = []
    for i in range(0, len(bits) - 7, 8):
        byte = bits[i:i+8]
        ch = chr(int(byte, 2))
        if ch == 'þ':
            break
        chars.append(ch)
    return ''.join(chars)

def decode_variants(image_path):
    image = Image.open(image_path).convert("RGBA")
    pixels = image.load()
    w, h = image.size

    coords_all = [(x, y) for y in range(h) for x in range(w)]
    coords_reverse = list(reversed(coords_all))
    coords_alpha255 = [(x, y) for x, y in coords_all if pixels[x, y][3] == 255]
    coords_alpha_under255 = [(x, y) for x, y in coords_all if pixels[x, y][3] < 255]
    coords_alpha_above0 = [(x, y) for x, y in coords_all if pixels[x, y][3] > 0]
    coords_alpha_sorted = sorted(coords_all, key=lambda c: pixels[c[0], c[1]][3])
    coords_alpha_rsorted = list(reversed(coords_alpha_sorted))
    coords_skip_leading_alpha0 = []
    started = False
    for x, y in coords_all:
        if not started and pixels[x, y][3] == 0:
            continue
        started = True
        coords_skip_leading_alpha0.append((x, y))

    # Define decoding strategies
    variants = {
        "alpha255":        (coords_alpha255, (0,1,2)),
        "alphaBelow255":   (coords_alpha_under255, (0,1,2)),
        "alphaAbove0":     (coords_alpha_above0, (0,1,2)),
        "alphaSorted":     (coords_alpha_sorted, (0,1,2)),
        "alphaRevSorted":  (coords_alpha_rsorted, (0,1,2)),
        "forward":         (coords_all, (0,1,2)),
        "reverse":         (coords_reverse, (0,1,2)),
        "skipLeadingAlpha0": (coords_skip_leading_alpha0, (0,1,2)),
    }

    base_name = os.path.splitext(os.path.basename(image_path))[0]

    for label, (coord_list, channels) in variants.items():
        bits = extract_bits(pixels, coord_list, channels)
        msg = bits_to_string(bits)
        output_file = f"{base_name}_{label}.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(msg)
        print(f"✅ {label} -> {output_file}")
        print("🔍 Preview:", msg[:100])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python decode_all_variants.py <imagefile>")
        sys.exit(1)

    img_path = sys.argv[1]
    if not os.path.isfile(img_path):
        print(f"File not found: {img_path}")
        sys.exit(1)

    decode_variants(img_path)
