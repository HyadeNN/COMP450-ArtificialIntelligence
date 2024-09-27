########################################################
# Hüseyin Efe Karagöz // Comp 450 // Week 2 // Task 2D #
########################################################

import random

# Initialize the board
board = [[' ' for _ in range(3)] for _ in range(3)]
old_wins, a_star_wins, draws = 0, 0, 0

# Function to print the board
def print_board():
    for row in board:
        print("|".join(row))
        print("-" * 5)

# Function to reset the board
def reset_board():
    global board
    board = [[' ' for _ in range(3)] for _ in range(3)]

# Function to check for a winner
def check_winner(player):
    for i in range(3):
        if all([cell == player for cell in board[i]]) or all([board[j][i] == player for j in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]) or all([board[i][2-i] == player for i in range(3)]):
        return True
    return False

# Check if the board is full
def is_full():
    return all([cell != ' ' for row in board for cell in row])

# Old Algorithm (Computer playing X)

# Computer's (X) first move - always play the center
def computer_first_move():
    board[1][1] = 'X'
    print("Old Algorithm (X) plays its first move at (1, 1)")
    print_board()

# Computer's second move based on the ruleset
def computer_second_move():
    # Check where "O" was placed (corner or side)
    player_move = [(i, j) for i in range(3) for j in range(3) if board[i][j] == 'O']
    if player_move:
        i, j = player_move[0]
        # If "O" is on a corner
        if (i, j) in [(0, 0), (0, 2), (2, 0), (2, 2)]:
            # Place X in a non-diagonal corner
            if i == j:
                board[0][2] = 'X'
            else:
                board[0][0] = 'X'
        # If "O" is on a side
        elif (i, j) in [(0, 1), (1, 0), (1, 2), (2, 1)]:
            # Place X in a corner next to the placed O
            if i == 0 and j == 1:
                board[0][0] = 'X'
            elif i == 1 and j == 0:
                board[0][0] = 'X'
            elif i == 1 and j == 2:
                board[0][2] = 'X'
            elif i == 2 and j == 1:
                board[2][0] = 'X'
        print("Old Algorithm (X) plays its second move:")
        print_board()

# Computer's third move - try to win or block player from winning
def computer_third_move():
    # Check if X can win, else block O
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'X'
                if check_winner('X'):
                    print("Old Algorithm (X) plays to win:")
                    print_board()
                    return True
                else:
                    board[i][j] = 'O'
                    if check_winner('O'):
                        board[i][j] = 'X'
                        print("Old Algorithm (X) blocks O:")
                        print_board()
                        return False
                    board[i][j] = ' '  # Undo the move
    # If no win/block, place X in a strategic spot
    print("Old Algorithm (X) plays its third move:")
    print_board()
    return False

# A* Algorithm (AI search for the best move)
def a_star_algorithm(player):
    best_score = float('-inf') if player == 'X' else float('inf')
    best_move = None

    # Recursive minimax function with heuristic
    def minimax(board, depth, is_maximizing, alpha, beta):
        if check_winner('X'):
            return 10 - depth
        if check_winner('O'):
            return depth - 10
        if is_full():
            return 0

        if is_maximizing:
            max_eval = float('-inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = 'X'
                        eval = minimax(board, depth + 1, False, alpha, beta)
                        board[i][j] = ' '
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            return max_eval
        else:
            min_eval = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = 'O'
                        eval = minimax(board, depth + 1, True, alpha, beta)
                        board[i][j] = ' '
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return min_eval

    # A* Algorithm picks the best move by evaluating all possible moves
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = player
                score = minimax(board, 0, player == 'O', float('-inf'), float('inf'))
                board[i][j] = ' '
                if player == 'X':
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
                else:
                    if score < best_score:
                        best_score = score
                        best_move = (i, j)

    if best_move:
        board[best_move[0]][best_move[1]] = player
        print(f"A* Algorithm ({player}) plays at ({best_move[0]}, {best_move[1]})")
        print_board()

# Player's move input
def player_move(player):
    while True:
        try:
            x = int(input(f"Next move X position for {player} (0, 1, 2): "))
            y = int(input(f"Next move Y position for {player} (0, 1, 2): "))
            if board[x][y] == ' ':
                board[x][y] = player
                break
            else:
                print("That spot is already taken. Try again.")
        except (ValueError, IndexError):
            print("Invalid input. Try again.")
    print_board()

# Main function to handle game mode and play games
def play_game():
    global old_wins, a_star_wins, draws
    print("Choose mode:")
    print("1. Player vs Old Algorithm")
    print("2. Player vs A* Algorithm")
    print("3. Old Algorithm vs A* Algorithm")
    mode = int(input("Enter the mode number: "))

    for game in range(1, 1001):  # Run 100 games for AI vs AI mode
        reset_board()
        print(f"Game {game}:")
        if mode == 1:  # Player vs Old Algorithm
            computer_first_move()
            while True:
                player_move('O')
                if is_full():
                    print("It's a draw!")
                    draws += 1
                    break
                computer_second_move()
                if check_winner('X'):
                    print("Old Algorithm (X) wins!")
                    old_wins += 1
                    break
                elif check_winner('O'):
                    print("Player (O) wins!")
                    break
                if is_full():
                    print("It's a draw!")
                    draws += 1
                    break
                if not computer_third_move():
                    if check_winner('O'):
                        print("Player (O) wins!")
                        break

        elif mode == 2:  # Player vs A* Algorithm
            while True:
                player_move('O')
                a_star_algorithm('X')
                if check_winner('X'):
                    print("A* Algorithm (X) wins!")
                    a_star_wins += 1
                    break
                elif check_winner('O'):
                    print("Player (O) wins!")
                    break
                if is_full():
                    print("It's a draw!")
                    draws += 1
                    break

        elif mode == 3:  # Old Algorithm vs A* Algorithm
            computer_first_move()
            while True:
                a_star_algorithm('O')
                if check_winner('O'):
                    print("A* Algorithm (O) wins!")
                    a_star_wins += 1
                    break
                elif check_winner('X'):
                    print("Old Algorithm (X) wins!")
                    old_wins += 1
                    break
                if is_full():
                    print("It's a draw!")
                    draws += 1
                    break
                if not computer_third_move():
                    if check_winner('X'):
                        print("Old Algorithm (X) wins!")
                        old_wins += 1
                        break
                if is_full():
                    print("It's a draw!")
                    draws += 1
                    break

    if mode == 3:
        print(f"Old Algorithm Wins: {old_wins}, A* Algorithm Wins: {a_star_wins}, Draws: {draws}")

play_game()
