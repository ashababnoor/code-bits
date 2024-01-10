'''
This script runs a simulation on the Monty Hall problem.

Problem description:
The Monty Hall problem is a probability puzzle based on a game show scenario. 
In the game, there are three doors, behind one of which is a valuable prize, 
and behind the other two are goats. The contestant initially chooses one door. 
After the contestant makes their choice, the host, who knows what is behind 
each door, opens one of the remaining doors to reveal a goat. The contestant is 
then given the option to switch their choice to the other unopened door or stick 
with their original choice. The question is: What is the optimal strategy for 
the contestant to maximize their chances of winning the prize?

This script simulates the Monty Hall problem by running multiple trials. 
In each trial, the script randomly selects a door for the prize, the contestant's 
initial choice, and the door to be revealed by the host. It then calculates the 
probabilities of winning with and without switching the chosen door. The simulation 
is run for a specified number of trials and the resulting probabilities are printed.
'''

import random

def monte_hall_simulation(num_trials):
    wins_with_switch = 0
    wins_without_switch = 0

    for _ in range(num_trials):
        # Randomly choose the door with the prize
        prize_door = random.randint(1, 3)

        # Randomly choose the door the contestant picks
        contestant_door = random.randint(1, 3)

        # Randomly choose a door to reveal that doesn't have the prize
        revealed_door = random.choice([door for door in range(1, 4) if door != prize_door and door != contestant_door])

        # Switch the contestant's door to the remaining unopened door
        switched_door = [door for door in range(1, 4) if door != contestant_door and door != revealed_door][0]

        # Check if the contestant wins with or without switching
        if switched_door == prize_door:
            wins_with_switch += 1
        if contestant_door == prize_door:
            wins_without_switch += 1

    # Calculate the winning probabilities
    switch_probability = wins_with_switch / num_trials
    no_switch_probability = wins_without_switch / num_trials

    return switch_probability, no_switch_probability

# Run the simulation with 10000 trials
switch_prob, no_switch_prob = monte_hall_simulation(10000)
print(f"Probability of winning with switch: {switch_prob}")
print(f"Probability of winning without switch: {no_switch_prob}")
