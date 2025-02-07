def is_prime(n):
    count=0
    if n <= 1:
        return False
    for i in range(1, n+1):
        if n%i==0:
            count+=1
    if count==2:
        return True

def filter_prime(numbers):
    return [num for num in numbers if is_prime(num)]

print(filter_prime([2, 3, 4, 5, 6, 7, 8, 9, 10]))