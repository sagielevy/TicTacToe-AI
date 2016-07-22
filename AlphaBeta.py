from Constants import  MAX_PLAYER_TYPE, MIN_PLAYER_TYPE


class Node(object):
    def __init__(self, board, row_count, col_count, diag_count, maximizing_player, move):
        self.type = MAX_PLAYER_TYPE if maximizing_player else MIN_PLAYER_TYPE
        self.maximizing_player = maximizing_player
        self.board = board
        self.row_count = row_count
        self.col_count = col_count
        self.diag_count = diag_count
        self.move = move
        self.v = self.calc_heuristic()

    def is_leaf(self):
        # Leaf if victory/lose/tie
        return abs(self.v) == 3 or (0 not in self.board)

    def gen_children(self):
        for i, cell in enumerate(self.board):
            if cell == 0:
                # Same board with single move change
                child_board = list(self.board)
                child_board[i] = self.type

                child_row_count = list(self.row_count)
                child_col_count = list(self.col_count)
                child_diag_count = list(self.diag_count)

                # Update counts
                child_row_count[i / 3] += self.type
                child_col_count[i % 3] += self.type

                # A cell that is on one of the diagonal lines
                if i % 2 == 0:
                    # Middle cell for both diagonal lines
                    if i == 4:
                        child_diag_count[0] += self.type
                        child_diag_count[1] += self.type
                    else:
                        # Left to right diagonal in cell 0 (divided by 2 give even result),
                        # opposite in cell 1 (give odd result)
                        child_diag_count[0 if (i / 2) % 2 == 0 else 1] += self.type

                yield Node(child_board, child_row_count, child_col_count, child_diag_count,
                           not self.maximizing_player, i)

    def calc_heuristic(self):
        # Select evaluation type
        eval_op = max if self.maximizing_player else min

        # Best value from all options
        return eval_op(self.row_count + self.col_count + self.diag_count)


def ab(node, depth, a, b, maximizing_player):
    """
    Step 1. Call this method on AI turn.
    Step 2. ???
    Step 3. Profit!
    """

    if depth == 0 or node.is_leaf():
        return node.v, node.move

    if maximizing_player:
        # Negative infinity flag, aka worse case scenario for maximizer
        v = -float("inf")
        result = node.move

        for child in node.gen_children():
            v = max(v, ab(child, depth - 1, a, b, False)[0])

            # Best new move found, update result for root node
            if v > a and node.move == -1:
                result = child.move

            a = max(v, a)

            if b <= a:
                break

        return v, result
    else:
        # Positive infinity flag, aka worse case scenario for minimizer
        v = float("inf")
        result = node.move

        for child in node.gen_children():
            v = min(v, ab(child, depth - 1, a, b, True)[0])

            # Best new move found, update result for root node
            if v < b and node.move == -1:
                result = child.move

            b = min(v, b)

            if b <= a:
                break

        return v, result
