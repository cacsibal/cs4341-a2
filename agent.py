from board import Board
from uttt import UltimateTicTacToe

from typing import Tuple
from collections.abc import Callable
# You may import additional standard packages (like math for your eval function).

def eval(state: Board, player: str) -> float:
    '''
    This function should calculate the heuristic score of a given Ultimate Tic-Tac-Toe board state from the perspective of the specified player.

    Parameters:
        state (Board): The current game board.
        player (str): The player symbol ("X" or "O") whose perspective the evaluation is based on.

    Returns:
        float: The heuristic score of the board state, where higher values favor the given player.
    '''
    opponent = 'O' if player == 'X' else 'X'
    score = 0
    for sup_r in range(3):
        for sup_c in range(3):
            sub = state.cells[sup_r][sup_c]
            if isinstance(sub, list):
                player_count = sum(
                    1 for sub_r in range(3) for sub_c in range(3) if sub[sub_r][sub_c] == player
                )
                opponent_count = sum(
                    1 for sub_r in range(3) for sub_c in range(3) if sub[sub_r][sub_c] == opponent
                )
                score += (player_count ** 2) - (opponent_count ** 2)
            elif sub == player:
                score += 81
            elif sub == opponent:
                score -= 81
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
        self.node_count = 0

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

    def max_value(self, state: Board, alpha: float, beta: float, depth: int) -> Tuple[float, Tuple[int, int, int, int]]:
        self.node_count += 1

        if UltimateTicTacToe.is_terminal(state):
            return self.eval(state, self.player), None

        if depth >= self.depth_limit:
            return self.eval(state, self.player), None

        v = float('-inf')
        best_action = None

        for action in UltimateTicTacToe.actions(state):
            result = UltimateTicTacToe.result(state, action)
            v2, a2 = self.min_value(result, alpha, beta, depth + 1)
            if v2 > v:
                v = v2
                best_action = action
                alpha = max(alpha, v)

            if v >= beta:
                break
        return v, best_action

    def min_value(self, state: Board, alpha: float, beta: float, depth: int) -> Tuple[float, Tuple[int, int, int, int]]:
        self.node_count += 1

        if UltimateTicTacToe.is_terminal(state):
            return self.eval(state, self.player), None

        if depth >= self.depth_limit:
            return self.eval(state, self.player), None

        v = float('inf')
        best_action = None

        for action in UltimateTicTacToe.actions(state):
            result = UltimateTicTacToe.result(state, action)
            v2, a2 = self.max_value(result, alpha, beta, depth + 1)
            if v2 < v:
                v = v2
                best_action = action
                beta = min(beta, v)

            if v <= alpha:
                break
        return v, best_action