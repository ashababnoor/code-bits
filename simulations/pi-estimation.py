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
