# https://www.hackerrank.com/challenges/grading

#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'gradingStudents' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts INTEGER_ARRAY grades as parameter.
#

def gradingStudents(grades):
    changedGrades = []
    for grade in grades:
        if grade < 38:
            changedGrades.append(grade)
        elif grade%5 == 0:
            changedGrades.append(grade)
        else:
            nextQ = grade//5 + 1
            if nextQ*5 - grade < 3:
                changedGrades.append(nextQ*5)
            else:
                changedGrades.append(grade)
                
    return changedGrades

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    grades_count = int(input().strip())

    grades = []

    for _ in range(grades_count):
        grades_item = int(input().strip())
        grades.append(grades_item)

    result = gradingStudents(grades)

    fptr.write('\n'.join(map(str, result)))
    fptr.write('\n')

    fptr.close()
