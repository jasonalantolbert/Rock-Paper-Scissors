# Rock Paper Scissors
# Author: Jason Tolbert (https://github.com/jasonalantolbert)
# Python Version: 3.8


# BEGINNING OF PROGRAM

# Imports the random and re modules.
import random
import re

# Creates global variables for the user's score and the list of enabled moves.
user_score = 0
global_moves = []

# Asks the user for their name and prints "Hello, {user_name}".
user_name = input("Enter your name: ")
print(f"Hello, {user_name}")


def scorekeeper_start(user):
    # Checks to see if the user has an existing record in rating.txt. If they do, user_score is set
    # to the value of the existing record. Otherwise, it's left at 0.
    with open("rating.txt", "r") as score_log:
        for record in score_log:
            name, score = record.rstrip("\n").split()

            if name == user:
                global user_score
                user_score = int(score)
                return


def get_moves(*game_moves):
    # Takes the list of moves the user enabled for the game and puts them in the global_moves list.
    # Additionally, it compiles those moves into a regular expression object for input validation
    # when user is asked to make a move later on.
    global global_moves
    global_moves = game_moves[0]
    regex_moves_list = []

    for option in game_moves[0]:
        regex_moves_list.append(f"^{option}$")
    regex_moves_pattern = re.compile("|".join(regex_moves_list))
    return regex_moves_pattern


def scorekeeper(status):
    # Modifies user_score based on game result.
    # +50 points for a draw, +100 points for a win, no change for a loss.
    global user_score

    if status == "draw":
        user_score += 50
    elif status == "win":
        user_score += 100


def cpu_move():
    # Randomly selects the computer's move from the list of moves the user enabled for the game.
    return random.choice(global_moves)


def get_result(user_move, computer_move):
    # Determines the game result.
    winning_cases = {
        # Credit to Dostonbek Matyakubov (https://hyperskill.org/profile/40038212)
        # for the winning_cases dictionary.
        'water': ['scissors', 'fire', 'rock', 'gun', 'lightning', 'devil', 'dragon'],
        'dragon': ['snake', 'scissors', 'fire', 'rock', 'gun', 'lightning', 'devil'],
        'devil': ['tree', 'human', 'snake', 'scissors', 'fire', 'rock', 'gun'],
        'gun': ['wolf', 'tree', 'human', 'snake', 'scissors', 'fire', 'rock'],
        'rock': ['sponge', 'wolf', 'tree', 'human', 'snake', 'scissors', 'fire'],
        'fire': ['paper', 'sponge', 'wolf', 'tree', 'human', 'snake', 'scissors'],
        'scissors': ['air', 'paper', 'sponge', 'wolf', 'tree', 'human', 'snake'],
        'snake': ['water', 'air', 'paper', 'sponge', 'wolf', 'tree', 'human'],
        'human': ['dragon', 'water', 'air', 'paper', 'sponge', 'wolf', 'tree'],
        'tree': ['devil', 'dragon', 'water', 'air', 'paper', 'sponge', 'wolf'],
        'wolf': ['lightning', 'devil', 'dragon', 'water', 'air', 'paper', 'sponge'],
        'sponge': ['gun', 'lightning', 'devil', 'dragon', 'water', 'air', 'paper'],
        'paper': ['rock', 'gun', 'lightning', 'devil', 'dragon', 'water', 'air'],
        'air': ['fire', 'rock', 'gun', 'lightning', 'devil', 'dragon', 'water'],
        'lightning': ['tree', 'human', 'snake', 'scissors', 'fire', 'rock', 'gun']
    }

    if user_move == computer_move:
        # If the user and the computer made the same move, it's a draw.
        scorekeeper("draw")
        return f"There is a draw ({computer_move})"
    else:
        # If the computer's move is in the list assigned to the dictionary key
        # in winning_cases that corresponds to the user's move, the user wins.
        for case in winning_cases[user_move]:
            if case == computer_move:
                scorekeeper("win")
                return f"Well done. The computer chose {computer_move} and failed"
        # If it's not a draw and the user didn't win, then by process of
        # elimination, the user loses.
        return f"Sorry, but the computer chose {computer_move}"


def game_control_loop(valid_moves):
    # Functions as the master control for the game.
    while True:
        # This loop - and by extension, this program - runs infinitely.

        global user_score

        user_choice = input()  # Here, the user will enter either a move, !rating, or !exit.

        if user_choice == "!exit":
            # If the user enters !exit, the program prints "Bye!" and quits.
            # The program will run infinitely until this occurs.
            print("Bye!")
            exit()
        elif user_choice == "!rating":
            # If the user enters !rating, the program prints their score.
            print(f"Your rating: {user_score}")
        elif valid_moves.match(user_choice):
            # If the user enters a valid move as determined by the valid_moves
            # regular expression object, the program compares the user's move
            # to the computer's move, determines the result, and prints it.
            print(get_result(user_choice, cpu_move()))
        else:
            # If the user's input does not match any of the above conditions,
            # the program prints "Invalid input".
            print("Invalid input")


def game_initialization():
    # Gathers the initial data needed for the game to function.
    global user_name
    scorekeeper_start(user_name)
    # Calls scorekeeper_start() with the user's name as an argument.
    enabled_moves = input("Enter a comma-separated list of moves to be enabled for this game.\n")
    # Asks the user what moves they want to be enabled for the game.
    print("Okay, let's start")
    if enabled_moves:
        # If the user entered any moves, they will be passed as an argument
        # to get_moves(), and the output of that function will be passed
        # as an argument to game_control_loop().
        game_control_loop(get_moves(enabled_moves.split(",")))
    else:
        # If the user didn't enter any moves, the game defaults to rock, paper and scissors.
        game_control_loop(get_moves("rock,paper,scissors".split(",")))


# Calls game_initialization(). Everything starts here.
game_initialization()


# END OF PROGRAM
