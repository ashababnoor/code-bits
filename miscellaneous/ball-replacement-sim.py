'''
This scripts runs a simulation on a ball replacement problem.

Problem description: 
You have a bag containing 20 blue and 13 red balls. You randomly select
two balls without replacement and depending on whether they are the same
color or different colors, you replace them with a blue or red ball
respectively. The balls that you take out are not returned to the bag, so the
number of balls in the bag decreases each time. What color will be the last
ball remaining in the bag?
'''

import random

init_no_of_blue_balls = 20
init_no_of_red_balls = 13

blue_balls_remaining = init_no_of_blue_balls
red_balls_remaining = init_no_of_red_balls

blue_ball = 'blue_ball'
red_ball = 'red_ball'

normal_choices = [blue_ball, red_ball]
only_blue_choices = [blue_ball]
only_red_choices = [red_ball]

while True:
    # checking if i have at least two balls remaining
    total_balls_remaining = blue_balls_remaining + red_balls_remaining
    if total_balls_remaining < 2:
        break
    
    # choosing the first ball
    if blue_balls_remaining and red_balls_remaining:
        first_ball_chosen = random.choice(normal_choices)

    # reducing the number of balls based on what was chosen
    if first_ball_chosen == blue_ball:
        blue_balls_remaining -= 1
    else:
        red_balls_remaining -= 1

    # choosing the second ball 
    if blue_balls_remaining and red_balls_remaining:    
        second_ball_chosen = random.choice(normal_choices)
    elif blue_balls_remaining:
        second_ball_chosen = random.choice(only_blue_choices)
    elif red_balls_remaining:
        second_ball_chosen = random.choice(only_red_choices)
    else:
        break
    
    # reducing the number of balls based on what was chosen
    if second_ball_chosen == blue_ball:
        blue_balls_remaining -= 1
    else:
        red_balls_remaining -= 1
    
    # adding a ball based on what was chosen
    if first_ball_chosen == second_ball_chosen:
        blue_balls_remaining += 1
    else:
        red_balls_remaining += 1

print("Balls remaining:")
print("\t Blue balls -", blue_balls_remaining)
print("\t Red balls -", red_balls_remaining)


