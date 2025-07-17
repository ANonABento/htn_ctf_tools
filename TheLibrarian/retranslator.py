import json

# Load the reversed dictionary
with open("letter_dict_reverse.json", "r") as f:
    reverse_dict = json.load(f)

def translate_text(text):
    return "".join(reverse_dict.get(c, c) for c in text)

text = input("Enter text to decode: ")
print("Decoded:", translate_text(text))
