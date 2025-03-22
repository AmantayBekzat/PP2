import time
import math

x = int(input("Enter a number: "))
ms = int(input("Enter delay in milliseconds: "))

time.sleep(ms / 1000)

sqrt_value = math.sqrt(x)

print(f"Square root of {x} after {ms} milliseconds is {sqrt_value}")