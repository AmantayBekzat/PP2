def is_palindrome(text):
    return text == text[::-1]

text = input("Enter a word: ")

if is_palindrome(text):
    print("This is a palindrome!")
else:
    print("This is NOT a palindrome!")