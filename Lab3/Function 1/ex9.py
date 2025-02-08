import math

def sphere_volume(r):
    return (4 / 3) * math.pi * (r ** 3)
a=int(input())
print(sphere_volume(a))