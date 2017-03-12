from random import randrange
import time


#win sets - static information

#variables: board space, current player, list of players, winner, move - variables
move = None
board = [' ',' ',' ',' ',' ',' ',' ',' ',' ']

current_player = ""
winner = None

win_cons = ((0, 1, 2),(3, 4, 5),(6, 7, 8),(0, 3, 6),(1, 4, 7),(2, 5, 8),(0, 4, 8),(2, 4, 6))

#functions:

#check if valid move is made
def valid_move():
    global move
    move = int(move)
    #check that the space exists
    if move > 0 or move < 8: 
        #check that the space is free
        if board[move] is " ":
            return True
        else:
            print("That space is taken! Pick another.")
    else:
        print("You must enter a value between 0 and 8. Try again.")

#check if there is a win, loss or draw
def check_winstate():
    #check each row
    for row in win_cons:
        #do any of these rows match? are they all full?
        if board[row[0]] is board[row[1]] is board[row[2]] != ' ':
            #who won?
            return board[row[0]]
    if ' ' not in board:
        return "draw"
    #if neither condition is met, continue with the game
    return None

#get moves
def get_human():
    '''Get a human players raw input. Returns None if a number is not entered.'''
    return input();

def get_ai():
    #random AI
    return randrange(9)

#process input
def input():
    global move
    if current_player is "x":
        move = get_human()
    else:
        move = get_ai()

#update model
def update():
    if valid_move():
        board[move] = current_player
        winner = check_winstate()
        if current_player is "x":
            current_player = "o"
        else:
            current_player = "x"
        

#render
def render():
    print ("    " + board[0] + " | " + board[1] + " | " + board[2])
    print ("   -----------")
    print ("    " + board[3] + " | " + board[4] + " | " + board[5])
    print ("   -----------")
    print ("    " + board[6] + " | " + board[7] + " | " + board[8])

    if winner is None:
        print("It's " + current_player + "'s turn.")

def help():
    print("To make a move enter a number between 0 - 8 and press enter.")
    print("The number corresponds to a board position as illustrated:")
    print("    0 | 1 | 2")
    print("    ---------")
    print("    3 | 4 | 5")
    print("    ---------")
    print("    6 | 7 | 8")

    print("")

#--------------------main function starts here------------------------

if __name__ == "__main__":
    #intro
    print("Welcome to Tic-Tac-Toe!")
    help()
    
    #set current player to P1
    current_player = "x"
    #render
    render()
    
#gameloop
    while winner is None:
        input()
        update()
        render()

#after a win/loss
    if winner is "draw":
        print("It's a draw, that means you're both winners!")
    elif winner is "x":
        print("Human player wins! Congratulations!")
    elif winner is "o":
        print("AI wins, better luck next time!")
