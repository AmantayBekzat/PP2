import re

with open("row.txt", "r", encoding="utf-8") as file:
    text = file.readlines()
found=False

for line in text:
    line=line.strip()
    x=re.split(r'(?=[A-Z])', line)
    if len(x) > 1:
        print(x)
        found = True 

if not found:
    print("Not found")



