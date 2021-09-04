#!/bin/python3

import sys

t = int(input().strip())

for a0 in range(t):
    n = int(input().strip())
    # print('n:', n)
    threeCount = (n-1)//3
    # print('threeCount:', threeCount)
    fiveCount = (n-1)//5
    # print('fiveCount:', fiveCount)
    
    commonCount = (n-1)//(3*5)
    
    num = ((threeCount*(threeCount+1)*3) + (fiveCount*(fiveCount+1)*5) - (commonCount*(commonCount+1)*15))
    num = num >> 1
    print(num)
