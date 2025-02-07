prime = lambda n: n > 1 and all(n % i != 0 for i in range(2,n))
numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 15, 17, 19, 20]
prime_numbers = list(filter(prime, numbers))

print("Prime numbers:", prime_numbers)
