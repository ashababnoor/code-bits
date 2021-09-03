# https://www.hackerrank.com/challenges/append-and-delete

#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'appendAndDelete' function below.
#
# The function is expected to return a STRING.
# The function accepts following parameters:
#  1. STRING s
#  2. STRING t
#  3. INTEGER k
#

def appendAndDelete(s, t, k):
    result = False
    if s == '':
        result = (k - len(t))%2 == 0
    elif t == '':
        result = (k - len(s))%2 == 0
    elif s == t:
        if len(s)%2 == 0:
            if k%2 == 0:
                result = k > 1
            else:
                result = False
        else:
            result = k > 1
    else:
        sameFirst = 0
        if len(s) > len(t):
            for i in range(len(t)):
                if s[i] == t[i]:
                    sameFirst += 1
                else:
                    break
        else:
            for i in range(len(s)):
                if s[i] == t[i]:
                    sameFirst += 1
                else:
                    break
        
        changes = (len(t) - sameFirst) + (len(s) - sameFirst)
        if changes <= k:
            result = (k - changes)%2 == 0
        else:
            result = False
    
    if result:
        return 'Yes'
    else:
        return 'No'

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    s = input()

    t = input()

    k = int(input().strip())

    result = appendAndDelete(s, t, k)

    fptr.write(result + '\n')

    fptr.close()
