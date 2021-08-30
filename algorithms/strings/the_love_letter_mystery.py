# https://www.hackerrank.com/challenges/the-love-letter-mystery

#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'theLoveLetterMystery' function below.
#
# The function is expected to return an INTEGER.
# The function accepts STRING s as parameter.
#

def theLoveLetterMystery(s):
    
    # Write your code here
    c = 0
    n = len(s)
    for i in range(n//2):
        if s[i] != s[n-i-1]:
            m = abs(ord(s[i]) - ord(s[n-i-1]))
            c = c+m
    return c

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    q = int(input().strip())

    for q_itr in range(q):
        s = input()

        result = theLoveLetterMystery(s)

        fptr.write(str(result) + '\n')

    fptr.close()
