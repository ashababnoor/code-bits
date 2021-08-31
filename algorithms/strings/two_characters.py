# https://www.hackerrank.com/challenges/two-characters

#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'alternate' function below.
#
# The function is expected to return an INTEGER.
# The function accepts STRING s as parameter.
#

def alternate(s):
    chars = []
    maxLength = 0

    for char in s:
        if char not in chars:
            chars.append(char)

    print('chars:', chars)

    for l1 in chars[:-1]:
        ind = chars[:-1].index(l1)
        for l2 in chars[ind+1:]:
            remainingChars = list(filter(lambda c: c != l1 and c != l2, chars))
            print('remaining chars:', remainingChars, 'l1, l2:', l1, l2)
            
            test = s
            for char in remainingChars:
                test = list(filter(lambda c: c != char, test))
            print('test:', test)
            if isValid(test, l1, l2):
                temp = len(test)
                print('len:', temp)
                if temp > maxLength:
                    maxLength = temp

    return maxLength

def isValid(test, l1, l2):
    n = len(test)
    op1 = ''
    op2 = ''
    
    string = ''
    for char in test:
        string += char

    if n%2 == 0:
        op1 = (str(l1)+str(l2))*(n//2)
        print('op1:', op1)
        op2 = (str(l2)+str(l1))*(n//2)
        print('op2:', op2)
    else:
        op1 = (str(l1)+str(l2))*(n//2) + str(l1)
        print('op1:', op1)
        op2 = (str(l2)+str(l1))*(n//2) + str(l2)
        print('op2:', op2)

    print('checking for:', string)
        
    if string == op1:
        return True
    elif string == op2:
        return True
    else:
        return False

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    l = int(input().strip())

    s = input()

    result = alternate(s)

    fptr.write(str(result) + '\n')

    fptr.close()
