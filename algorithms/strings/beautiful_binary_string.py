# https://www.hackerrank.com/challenges/beautiful-binary-string

#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'beautifulBinaryString' function below.
#
# The function is expected to return an INTEGER.
# The function accepts STRING b as parameter.
#

def beautifulBinaryString(b):
    c = 0
    for i in range(len(b)-2):
        if b[i:i+3] == '010':
            c += 1
            b = b[:i+2]+'1'+b[i+3:]
    return c

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = int(input().strip())

    b = input()

    result = beautifulBinaryString(b)

    fptr.write(str(result) + '\n')

    fptr.close()
