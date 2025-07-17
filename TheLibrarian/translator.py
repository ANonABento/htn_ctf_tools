import json

with open("letter_dict.json", "r") as f:
    letter_dict = json.load(f)

def translate_text(text):
    # Only maps original → translated letter, no reverse
    return "".join(letter_dict.get(c, c) for c in text)

text = input("Enter text to translate: ")
print("Translation:", translate_text(text))
