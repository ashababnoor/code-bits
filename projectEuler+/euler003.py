#!/bin/python3

import sys


def isPrime(num):
    if num < 2:
        return False
    elif num == 2:
        return True
    elif num % 2 == 0:
        return False
    else:
        upperlimit = int(num**0.5) + 1
        for i in range(3, upperlimit, 2):
            if num % i == 0:
                return False
        return True

t = int(input().strip())
for a0 in range(t):
    n = int(input().strip())
    if isPrime(n):
        print(n)
    else:
        upperlimit = n//2
        for i in range(upperlimit+1, 2, -1):
            if n % i == 0 and isPrime(i):
                print(i)
                break

    

