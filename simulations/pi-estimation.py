
'''
This script runs a simulation on estimating the value of Pi using Monte Carlo simulation.

Problem description:
The Monte Carlo simulation is a computational algorithm that relies on repeated random 
sampling to obtain numerical results. The underlying concept is to use randomness to 
solve problems that might be deterministic in principle. It is often used when the model 
or system is complex and cannot be easily solved directly or analytically. 

We want to estimate the value of Pi using the Monte Carlo simulation method. In this method, 
random points are generated within a square with side length 2. The square is centered at 
the origin (0, 0) and has corners at (-1, -1) and (1, 1). The ratio of the number of points 
that fall within a quarter of a circle inscribed in the square to the total number of points
generated is used to estimate the value of Pi. The estimation is based on the fact that the 
area of the quarter circle is Pi/4 and the area of the square is 4. Therefore, the ratio of 
the areas is Pi/4 / 4 = Pi/16. Multiplying this ratio by 4 gives an estimate of Pi.
'''

import random

def estimate_pi(num_points):
    points_inside_circle = 0
    points_total = 0

    for _ in range(num_points):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        distance = x**2 + y**2

        if distance <= 1:
            points_inside_circle += 1

        points_total += 1

    pi_estimate = 4 * points_inside_circle / points_total
    return pi_estimate

num_points = 1000000
pi_estimate = estimate_pi(num_points)
print("Estimated value of Pi:", pi_estimate)
