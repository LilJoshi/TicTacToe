### Tic-Tac-Toe, via 3x3 Magic Square (numbers 0-8)
### X is always first player

import random

#Players
O = 'O'
X = 'X'
N = ' '

other = lambda player: O if player is X else X

board = [N] * 9
transform = {0:7, 1:2, 2:3, 3:0, 4:4, 5:8, 6:5, 7:6, 8:1}

def print_board():
    print(board[7] + " | " + board[2] + " | " + board[3] + "\n" +
          "---------\n" +
          board[0] + " | " + board[4] + " | " + board[8] + "\n" +
          "---------\n" + 
          board[5] + " | " + board[6] + " | " + board[1])

opp = lambda position: 8 - position

center = [4]
corners = [7, 3, 5, 1]
sides = [2, 0, 8, 6]

def move(player, pos):
    if board[pos] is N:
        board[pos] = player
    else:
        raise Exception("can't play in occupied square")

def squares(player):
    """ Which squares (out of 9) are occupied by player = X? or O, N? """
    return [i for i in range(9) if board[i] == player]

def doubles(s):
    for x in range(len(s)):
        for y in range(x+1, len(s)):
            yield {s[x], s[y]}
            
def triples(s):
    for x in range(len(s)):
        for double in doubles(s[x+1:]):
            double.add(s[x])
            yield double

def winner(player):
    return any(sum(trip) == 12 for trip in triples(squares(player)))


def quickdraw():
    return not (any(sum(trip) == 12 for trip in triples(squares(X) + squares(N)))
        or any(sum(trip) == 12 for trip in triples(squares(O) + squares(N))))

# draw = lambda: squares(N) == []

def about_to_win(player):
    """ Yields position of move where player is about to win, otherwise False. """
    for move in squares(N):
        if any(sum(trip) == 12 - move for trip in doubles(squares(player))):
            return move
    return False

def turn():
    return X if squares(N) % 2 == 1 else O

def reset():
    for i in range(len(board)):
        board[i] = N

def prompt_game():
    reset()
    print("This is how you enter moves:")
    print("0 | 1 | 2\n---------\n3 | 4 | 5\n---------\n6 | 7 | 8\n")
    print("Begin.")


def run_game(p1, p2):
    prompt_game()
    curr_player = X
    strategy = p1
    while True:
        print_board()
        print(curr_player + "'s turn.")
        x = strategy(curr_player)
        move(curr_player, x)
        if winner(X) or winner(O) or quickdraw():
            break
        curr_player = other(curr_player)
        strategy = p2 if (strategy is p1) else p1
    print_board()
    if winner(X):
        print("X won!")
    elif winner(O):
        print("O won!")
    else:
        print("It's a draw!")

human = lambda player: transform[int(input("Where do you want to play, " + 
    player + "? " ))]

cpu_easy = lambda player: random.choice(squares(N))

def cpu_medium(player):
    abt = about_to_win(player) or about_to_win(other_player(player))
    if abt: return abt

    if all(x is N for x in board):
        return random.choice(corners)
    elif board[4] is N:
        return 4
    else:
        return random.choice(squares(N))

cpu = cpu_easy
simulation_game = lambda: run_game(cpu, cpu)
two_players = lambda: run_game(human, human)
single_player_as_x = lambda: run_game(human, cpu)
single_player_as_o = lambda: run_game(cpu, human)

def main():
    single_player_as_x()

main()
    
