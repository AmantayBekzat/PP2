import re

def snake_to_camel(snake_str):
    words = snake_str.split("_")
    return words[0].lower() + "".join(word.title() for word in words[1:])

with open("row.txt", "r", encoding="utf-8") as file:
    text = file.readlines()
found=False

for line in text:
    line=line.strip()
    if '_' in line:    
        x = snake_to_camel(line)
        print(x)
        found = True

if not found:
    print("Not found")



