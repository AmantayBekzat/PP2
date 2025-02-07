def palindrome(s):
    s = s.strip().lower()
    return s == s[::-1]

word=input()
print(palindrome(word))