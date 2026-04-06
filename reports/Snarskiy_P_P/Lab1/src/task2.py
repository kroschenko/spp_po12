"""Checking if phrase is palindrome"""


def check_palindrome():
    """Checking if phrase is palindrome"""
    s = input("Enter a phrase: ")
    s = s.lower()
    s = "".join(c for c in s if c.isalnum())
    ans = s == s[::-1]
    if ans:
        print("String is palindrome")
    else:
        print("String is not palindrome")


check_palindrome()
