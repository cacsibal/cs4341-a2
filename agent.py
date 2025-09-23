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
    raise(NotImplementedError)

class Agent:
    def __init__(self, player: str, eval: Callable[[Board, str], float], depth_limit: int) -> None:
        '''
        This method should initialize the Ultimate Tic-Tac-Toe agent with the given configuration.

        Parameters:
            player (str): The player symbol ("X" or "O") that the agent will control.
            eval (Callable[[Board, str], float]): A function that evaluates the desirability of a board state.
            depth_limit (int): The maximum search depth for the minimax algorithm with alpha-beta pruning.
        '''
        raise(NotImplementedError)

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
        raise(NotImplementedError)
