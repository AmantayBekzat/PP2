import re

with open("row.txt", "r", encoding="utf-8") as file:
    text = file.readlines()
found=False

for line in text:
    line=line.strip()
    x=re.findall(r"ab{2,3}",line)
    if x:
        print(x)
        found = True

if not found:
    print("Not found")



