#!/bin/python3

import sys


t = int(input().strip())
for a0 in range(t):
    n = int(input().strip())
    prev = 1
    curr = 2
    total = 0
    while curr < n:
        if curr%2==0:
            total += curr
        temp = curr
        curr = curr + prev
        prev = temp
    print(total)