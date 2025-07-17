import json
import os

def build_letter_dict(original_text, translated_text, existing_dict=None):
    original_text = original_text.replace("\n", "")
    translated_text = translated_text.replace("\n", "")

    if len(original_text) != len(translated_text):
        raise ValueError(f"Length mismatch: original({len(original_text)}) vs translated({len(translated_text)})")

    letter_dict = existing_dict or {}
    conflicts = {}

    for o_char, t_char in zip(original_text, translated_text):
        if o_char in letter_dict:
            if letter_dict[o_char] != t_char:
                conflicts.setdefault(o_char, set()).add(letter_dict[o_char])
                conflicts[o_char].add(t_char)
        else:
            letter_dict[o_char] = t_char  # Only one-way

    if conflicts:
        print("⚠️ Conflicts found for letters:")
        for c, mapped_set in conflicts.items():
            print(f"  '{c}' → {mapped_set}")

    return letter_dict

# Load existing letter_dict.json if it exists
if os.path.exists("letter_dict.json"):
    with open("letter_dict.json", "r") as f:
        existing_dict = json.load(f)
else:
    existing_dict = {}

print("Paste original text:")
orig = input()

print("Paste translated text:")
trans = input()

# Build or update dictionary
mapping = build_letter_dict(orig, trans, existing_dict)

# Save merged dictionary
with open("letter_dict.json", "w") as f:
    json.dump(mapping, f, indent=2)

print("Letter dictionary merged and saved as letter_dict.json")
