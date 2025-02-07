from itertools import permutations

def permutation(s):
    perms = [''.join(p) for p in permutations(s)]
    for perm in perms:
        print(perm)

string=input()
permutation(string)