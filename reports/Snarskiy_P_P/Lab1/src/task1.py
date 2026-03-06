"""
Generating sequence from start to end with step
"""


def rep():
    """function to generate sequence from start to end with step"""
    start = int(input("Enter a starting number: "))
    end = int(input("Enter an ending number: "))
    step = int(input("Enter a step: "))
    for i in range(start, end, step):
        print(i)


rep()
