import itertools
import numpy as np


def game_board(game_map, player=0, row=0, column=0, just_display=False):
    try:
        game_size = 3
        if game_map[row][column] != 0:
            print("Play a different position")
            return game_map, False

        print("   " + "  ".join([str(i) for i in range(len(game_map))]))

        if not just_display:
            game_map[row][column] = player
        for count, row in enumerate(game_map):
            print(count, row)
        return game_map, True
    except IndexError:
        print("Did you attempt to play a row or column\
                outside the range of 0,1 or 2? (IndexError)")
        return game_map, False
    except Exception as e:
        print(str(e))
        return game_map, False


def win(current_game):
    def all_same(l):
        if l.count(l[0]) == len(l) and l[0] != 0:
            return True
        else:
            return False

    # diagonal winner
    check_right = []
    check_left = []
    counter = 0

    for row in current_game:
        check_right.append(row[counter])
        check_left.append(row[len(current_game) - counter - 1])
        counter += 1
        print(row)

    if all_same(check_right):
        print(f"Player {row[0]} is the winner diagonally!")
        return True

    if all_same(check_left):
        print(f"Player {row[0]} is the winner diagonally!")
        return True

    # vertical winner
    for col in range(len(current_game)):
        check = []
        game_length = range(len(current_game))
        for row in current_game:
            check.append(row[col])
            print(row)

        if all_same(check):
            print(f"Player {row[col]} is the winner vertically!")
            return True

    # horizontal winner
    for row in current_game:
        print(row)
        if all_same(row):
            print(f"Player {row[0]} is the winner horizontally!")
            return True

    return False


play = True
players = [1, 2]

while play:
    game = [[0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]]

    game_won = False
    game, _ = game_board(game, just_display=True)
    player_choice = itertools.cycle([1, 2])
    while not game_won:
        current_player = next(player_choice)
        print(f"Current player: {current_player}")
        played = False

        while not played:
            column_choice = int(input("What column do you want to play? (0, 1, 2):"))
            row_choice = int(input("Which row do you want to play? (0, 1, 2):"))
            game, played = game_board(game, current_player, row_choice, column_choice,
                                      just_display=False)
            if game:
                played = True
        if win(game):
            game_won = True
            again = input("Game over, play again?")
            if again.lower() == "y":
                print("restarting")
            else:
                play = False
