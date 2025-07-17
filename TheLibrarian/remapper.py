import json

# Load the forward letter mapping
with open("letter_dict.json", "r") as f:
    forward_dict = json.load(f)

# Reverse it: value → key
reverse_dict = {}
conflicts = {}

for key, value in forward_dict.items():
    if value in reverse_dict:
        if reverse_dict[value] != key:
            conflicts.setdefault(value, set()).add(reverse_dict[value])
            conflicts[value].add(key)
    else:
        reverse_dict[value] = key

# Warn about any conflicts
if conflicts:
    print("⚠️ Conflicts found in reverse mapping:")
    for val, keys in conflicts.items():
        print(f"  '{val}' maps to multiple: {keys}")

# Save reversed dictionary
with open("letter_dict_reverse.json", "w") as f:
    json.dump(reverse_dict, f, indent=2)

print("✅ Reversed mapping saved to letter_dict_reverse.json")
