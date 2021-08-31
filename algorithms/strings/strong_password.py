# https://www.hackerrank.com/challenges/strong-password

#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'minimumNumber' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER n
#  2. STRING password
#

def minimumNumber(n, password):
    # Return the minimum number of characters to make the password strong
    numbers = "0123456789"
    lower_case = "abcdefghijklmnopqrstuvwxyz"
    upper_case = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    special_characters = "!@#$%^&*()-+"
    
    numCount = 0
    lowerCount = 0
    upperCount = 0
    specialCount = 0
    
    count = 0
    
    for char in password:
        if char in numbers:
            numCount += 1
        elif char in lower_case:
            lowerCount += 1
        elif char in upper_case:
            upperCount += 1
        elif char in special_characters:
            specialCount += 1
        
    if numCount == 0:
        count += 1
    if lowerCount == 0:
        count += 1
    if upperCount == 0:
        count += 1
    if specialCount == 0:
        count += 1
    
    if len(password) + count < 6:
        count = 6 - len(password)
        
    return count
    
    
if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = int(input().strip())

    password = input()

    answer = minimumNumber(n, password)

    fptr.write(str(answer) + '\n')

    fptr.close()
