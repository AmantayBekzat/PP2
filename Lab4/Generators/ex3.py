def num(n):
    result = []
    for i in range(n):
        if i % 3 == 0 and i % 4 == 0:
            result.append(i)
    return result

n = int(input("n:"))
k = num(n)
print(k)