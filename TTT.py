import AlphaBeta
from Constants import  MAX_PLAYER_TYPE, MIN_PLAYER_TYPE

board = [0, 0, 0,
         0, 0, 0,
         0, 0, 0]

row_count = [0, 0, 0]
col_count = [0, 0, 0]
diag_count = [0, 0]


def show_board():
    for i, cell in enumerate(board):
        if i % 3 == 0 and i > 0:
            print ""
        print str(cell) + ", ",
    print ""


def update_counters(i, p_type):
    # Update counts
    row_count[i / 3] += p_type
    col_count[i % 3] += p_type

    # A cell that is on one of the diagonal lines
    if i % 2 == 0:
        # Middle cell for both diagonal lines
        if i == 4:
            diag_count[0] += p_type
            diag_count[1] += p_type
        else:
            # Left to right diagonal in cell 0 (divided by 2 give even result), opposite in cell 1 (give odd result)
            diag_count[0 if (i / 2) % 2 == 0 else 1] += p_type


def user_input(p_type):
    show_board()

    try:
        pos = input("Enter i,j: ")
        i = pos[0] * 3 + pos[1]
    except SyntaxError:
        print "Write indices like a tuple!"

    while len(board) <= i or board[i] != 0:
        show_board()
        try:
            pos = input("Bad input. Enter i, j: ")
            i = pos[0] * 3 + pos[1]
        except SyntaxError:
            print "Write indices like a tuple!"

    # Set player choice
    board[i] = p_type

    # Show made move
    show_board()
    update_counters(i, p_type)


def start_game():
    if raw_input("Who goes first? Type 'p' for player or anything else for AI: ") == "p":
        user_input(MAX_PLAYER_TYPE)

    # Game ain't over, play AI move then player
    while 0 in board and all(x not in (3, -3) for x in (row_count + col_count + diag_count)):
        root = AlphaBeta.Node(tuple(board), tuple(row_count), tuple(col_count), tuple(diag_count), 0, -1)
        (v, result) = AlphaBeta.ab(root, 9, -float("inf"), float("inf"), root.maximizing_player)

        print "Best move found: " + str(v)
        print "AI to " + str(result / 3) + "," + str(result % 3)
        board[result] = MIN_PLAYER_TYPE
        update_counters(result, MIN_PLAYER_TYPE)
        show_board()
        print "\n"

        # Game still ain't over
        if 0 in board and all(x not in (3, -3) for x in (row_count + col_count + diag_count)):
            user_input(MAX_PLAYER_TYPE)

    # Game over by tie
    if 0 not in board:
        print "\nTie!"
    else:
        # Win, print winner
        if 3 in (row_count + col_count + diag_count):
            print "\nPlayer is the winner! This should never happen :O\nCall me up even if it's themiddleofthenite!@!"
        else:
            print "\nAI is the winner!"
    show_board()

if __name__ == "__main__":
    start_game()
