def indexOfDifference(str1, str2):
    if str1 is None or str2 is None:
        raise TypeError("Arguments cannot be None")
    
    if str1 == str2:
        return -1
    
    if not str1 or not str2:
        return 0
    
    # Сравниваем посимвольно до конца кратчайшей строки
    length = min(len(str1), len(str2))
    for i in range(length):
        if str1[i] != str2[i]:
            return i
            
    return length