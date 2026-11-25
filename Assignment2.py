
# Tic-Tac-Toe using Minimax with Alpha-Beta Pruning

import math

# Create empty board
board = [' ' for _ in range(9)]

# Display board
def display():
    for i in range(0, 9, 3):
        print(board[i], "|", board[i+1], "|", board[i+2])
        if i < 6:
            print("---------")

# Check winner
def check_winner():
    win = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]

    for a, b, c in win:
        if board[a] == board[b] == board[c] != ' ':
            return board[a]

    return None

# Minimax with Alpha-Beta Pruning
def minimax(is_max, alpha, beta):

    winner = check_winner()

    if winner == 'X':
        return 1
    elif winner == 'O':
        return -1
    elif ' ' not in board:
        return 0

    if is_max:
        best = -math.inf

        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(False, alpha, beta)
                board[i] = ' '

                best = max(best, score)
                alpha = max(alpha, best)

                if beta <= alpha:
                    break

        return best

    else:
        best = math.inf

        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(True, alpha, beta)
                board[i] = ' '

                best = min(best, score)
                beta = min(beta, best)

                if beta <= alpha:
                    break

        return best

# Find best move for computer
def best_move():
    best_score = -math.inf
    move = -1

    for i in range(9):
        if board[i] == ' ':
            board[i] = 'X'
            score = minimax(False, -math.inf, math.inf)
            board[i] = ' '

            if score > best_score:
                best_score = score
                move = i

    return move

# Main game
print("Tic-Tac-Toe Game")
print("You are O and Computer is X")

while True:
    display()

    # Computer move
    move = best_move()

    if move != -1:
        board[move] = 'X'

    if check_winner() == 'X':
        display()
        print("Computer Wins!")
        break

    if ' ' not in board:
        display()
        print("Game Draw!")
        break

    display()

    # Player move
    pos = int(input("Enter position (0-8): "))

    if pos < 0 or pos > 8 or board[pos] != ' ':
        print("Invalid position! Try again.")
        continue

    board[pos] = 'O'

    if check_winner() == 'O':
        display()
        print("You Win!")
        break

    if ' ' not in board:
        display()
        print("Game Draw!")
        break
