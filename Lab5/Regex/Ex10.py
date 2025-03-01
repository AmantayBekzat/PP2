import re

def camel_to_snake(camel_str):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', camel_str).lower()


with open("row.txt", "r", encoding="utf-8") as file:
    text = file.readlines()
found=False

for line in text:
    line=line.strip()
    x=camel_to_snake(line)
    print(x)
    found= True

if not found:
    print("Not found")



