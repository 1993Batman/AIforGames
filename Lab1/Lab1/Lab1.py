# Three state machine example ... bad code included.

# variables
import random
points = 0
stamina = 100

states = ['attack','defend','benched']
current_state = 'attack'

running = True
max_limit = 48
game_time = 0

while running:
    print("Time: " , game_time)
    print("Points: " , points)
    print("Stamina: " , stamina)

    if current_state is 'attack':
        # Do things for this state
        print("He SHOTS and...")
        ran_num = random.randrange(1,10)
        if ran_num < 5:
            points += 2
            stamina -= 4
            if game_time is 12 or game_time is 24 or game_time is 36 or game_time is 48:
                print("What a Buzzer Beater! Thats a clutch 2 point shot")
            else:
                print("Now thats a good 2 point shot")
        else:
            points += 3
            stamina -= 6
            if game_time is 12 or game_time is 24 or game_time is 36 or game_time is 48:
                print("What a Buzzer Beater! Thats a clutch 3 point shot")
            else:
                print("Now thats a good 3 point shot")
        current_state = 'defend'


    elif current_state is 'defend':
        print("They're on defence now...")
        ran_num = random.randrange(1,10)
        if ran_num < 5:
            stamina -= 6
            if game_time is 12 or game_time is 24 or game_time is 36 or game_time is 48:
                print("How did he block that one! Now thats a clutch defence at the end of the period")
            else:
                print("What a Block!!")
        else:
            stamina -= 4
            if game_time is 12 or game_time is 24 or game_time is 36 or game_time is 48:
                print("What a Play a steal on the buzzer which leads to an open 3")
                points += 3
            else:
                print("Now thats a nice steal")
        current_state = 'attack'
            

    elif current_state is 'benched':
        # Do things for this state
        print("You look tired... So you've been benched")
        stamina += 8
        # Check for change state
        if stamina > 85:
            current_state = 'attack'
            
    # check for broken ... :(
    else:
        print("AH! BROKEN .... how did you get here?")
        die() # not a real function - just breaks things! :)

    if stamina < 65:
        current_state = 'benched'
        
    # Check for end of game time
    if game_time >= max_limit:
        print('-- The Game Has Ended --')
        print("Time: " , game_time)
        print("Points: " , points)
        print("Stamina: " , stamina)
        running = False

    game_time += 1
