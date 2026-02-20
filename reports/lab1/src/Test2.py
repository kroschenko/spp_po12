def str_str(haystack, needle):
    if needle == "":
        return 0

    for i in range(len(haystack) - len(needle) + 1):
        if haystack[i : i + len(needle)] == needle:
            return i

    return -1


haystack = input("Enter a string: ")
needle = input("Enter a string: ")
print(str_str(haystack, needle))
