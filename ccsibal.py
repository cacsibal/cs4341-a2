from board import Board
from uttt import UltimateTicTacToe

from typing import Tuple
from collections.abc import Callable
# You may import additional standard packages (like math for your eval function).

def eval(state: Board, player: str) -> float:
    '''
    https://boardgames.stackexchange.com/questions/49291/strategy-for-ultimate-tic-tac-toe

    Parameters:
        state (Board): The current game board.
        player (str): The player symbol ("X" or "O") whose perspective the evaluation is based on.

    Returns:
        float: The heuristic score of the board state, where higher values favor the given player.
    '''
    opponent = 'O' if player == 'X' else 'X'

    # check for terminal game states first
    winner = state.get_winner()
    if winner == player:
        return float('inf')
    elif winner == opponent:
        return float('-inf')

    score = 0.0

    # get state of all super boards
    super_board = []
    for sup_r in range(3):
        row = []
        for sup_c in range(3):
            if isinstance(state.cells[sup_r][sup_c], str) and state.cells[sup_r][sup_c] != 'T':
                row.append(state.cells[sup_r][sup_c])
            else:
                row.append(None)
        super_board.append(row)

    # rule 2: count won/lost boards
    for sup_r in range(3):
        for sup_c in range(3):
            if super_board[sup_r][sup_c] == player:
                score += 100
            elif super_board[sup_r][sup_c] == opponent:
                score -= 100

    # rule 3: two boards in a row
    # check all possible lines on the super board
    lines = []

    for r in range(3):
        lines.append([super_board[r][c] for c in range(3)])

    for c in range(3):
        lines.append([super_board[r][c] for r in range(3)])

    # diagonals
    lines.append([super_board[i][i] for i in range(3)])
    lines.append([super_board[i][2 - i] for i in range(3)])

    for line in lines:
        player_count = line.count(player)
        opponent_count = line.count(opponent)
        none_count = line.count(None)

        # rule 3: two in a row for player
        if player_count == 2 and none_count == 1:
            score += 200

        # rule 3: two in a row for opponent
        if opponent_count == 2 and none_count == 1:
            score -= 200

    # rule 4: blocking opponent's three in a row
    # rule 5: winning a blocked board
    # check if winning a board blocks opponent or is blocked
    for sup_r in range(3):
        for sup_c in range(3):
            if super_board[sup_r][sup_c] == player:
                # check if board blocks opponent's lines
                temp_board = [row[:] for row in super_board]
                temp_board[sup_r][sup_c] = None  # remove our win temporarily

                # check all lines this position is part of
                position_lines = []
                position_lines.append([temp_board[sup_r][c] for c in range(3)])
                position_lines.append([temp_board[r][sup_c] for r in range(3)])
                if sup_r == sup_c: # diagonals
                    position_lines.append([temp_board[i][i] for i in range(3)])
                if sup_r + sup_c == 2:
                    position_lines.append([temp_board[i][2 - i] for i in range(3)])

                blocked_opponent = False
                is_blocked_by_opponent = False

                for line in position_lines:
                    if line.count(opponent) == 2 and line.count(None) == 1:
                        blocked_opponent = True  # rule 4: blocked opponent's win
                    if line.count(opponent) >= 1 and line.count(None) == 0:
                        is_blocked_by_opponent = True  # rule 5: line is blocked by opponent

                if blocked_opponent:
                    score += 150  # rule 4
                if is_blocked_by_opponent:
                    score -= 150  # rule 5

    # rules 6, 7, 8: analyze small boards
    for sup_r in range(3):
        for sup_c in range(3):
            if isinstance(state.cells[sup_r][sup_c], list):
                small_board = state.cells[sup_r][sup_c]

                # get all lines in the small board
                small_lines = []
                for r in range(3):
                    small_lines.append([small_board[r][c] for c in range(3)])
                for c in range(3):
                    small_lines.append([small_board[r][c] for r in range(3)])
                # diagonals
                small_lines.append([small_board[i][i] for i in range(3)])
                small_lines.append([small_board[i][2 - i] for i in range(3)])

                for line in small_lines:
                    player_count = line.count(player)
                    opponent_count = line.count(opponent)
                    none_count = line.count(None)

                    # rule 6: two in a row on small board
                    if player_count == 2 and none_count == 1:
                        score += 5

                    # rule 7: blocking win on small board
                    if opponent_count == 2 and none_count == 1:
                        score += 20

    return score

class Agent:
    def __init__(self, player: str, eval: Callable[[Board, str], float], depth_limit: int) -> None:
        '''
        This method should initialize the Ultimate Tic-Tac-Toe agent with the given configuration.

        Parameters:
            player (str): The player symbol ("X" or "O") that the agent will control.
            eval (Callable[[Board, str], float]): A function that evaluates the desirability of a board state.
            depth_limit (int): The maximum search depth for the minimax algorithm with alpha-beta pruning.
        '''
        self.player = player
        self.eval = eval
        self.depth_limit = depth_limit

    def search(self, state: Board) -> Tuple[float, Tuple[int, int, int, int], int]:
        '''
        This method should perform minimax search with alpha-beta pruning to determine the best move for the agent from the given board state.

        Parameters:
            state (Board): The current game board.

        Returns:
            float: The heuristic value of the best move.
            Tuple[int, int, int, int]: The best move (action) for the current player.
            int: The number of nodes evaluated during the search (equivalent to the total number of times the MAX-VALUE and MIN-VALUE functions were called).
        '''
        self.node_count = 0
        value, move = self.max_value(state, float('-inf'), float('inf'), 0)
        return value, move, self.node_count

    def minimax(self, state: Board, alpha: float, beta: float, depth: int, is_maximizing: bool) -> Tuple[float, Tuple[int, int, int, int]]:
        '''
        minimax function that handles both MAX and MIN nodes based on is_maximizing flag.

        Parameters:
            state: Current board state
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            depth: Current search depth
            is_maximizing: True for MAX nodes, False for MIN nodes

        Returns:
            Tuple of (best_value, best_action)
        '''
        self.node_count += 1

        if UltimateTicTacToe.is_terminal(state):
            return self.eval(state, self.player), None

        if depth >= self.depth_limit:
            return self.eval(state, self.player), None

        best_value = float('-inf') if is_maximizing else float('inf')
        best_action = None

        for action in UltimateTicTacToe.actions(state):
            result = UltimateTicTacToe.result(state, action)

            v2, a2 = self.minimax(result, alpha, beta, depth + 1, not is_maximizing)

            if is_maximizing:
                if v2 > best_value:
                    best_value = v2
                    best_action = action

                alpha = max(alpha, best_value)

                if best_value >= beta:
                    break
            else:
                if v2 < best_value:
                    best_value = v2
                    best_action = action

                beta = min(beta, best_value)

                if best_value <= alpha:
                    break

        return best_value, best_action

    def max_value(self, state: Board, alpha: float, beta: float, depth: int) -> Tuple[float, Tuple[int, int, int, int]]:
        return self.minimax(state, alpha, beta, depth, True)

    def min_value(self, state: Board, alpha: float, beta: float, depth: int) -> Tuple[float, Tuple[int, int, int, int]]:
        return self.minimax(state, alpha, beta, depth, False)
