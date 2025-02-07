def unique(l):
    elements= []
    for digit in l:
        if digit not in elements:
            elements.append(digit)
    return elements

print(unique([1,1,1,1,1,2,2,3,4,4,5,5,5,5,5,6,7,8,9,5,3]))