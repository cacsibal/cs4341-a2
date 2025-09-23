from typing import Tuple, List
from board import Board

class UltimateTicTacToe:
    @staticmethod
    def initial_state() -> Board:
        return Board()

    @staticmethod
    def to_move(state: Board) -> str:
        return state.next_player

    @staticmethod
    def actions(state: Board) -> List[Tuple[int, int, int, int]]:
        return state.get_legal_moves()

    @staticmethod
    def result(state: Board, move: Tuple[int, int, int, int]) -> Board:
        result_state = state.copy()
        result_state.place(*move)
        return result_state

    @staticmethod
    def is_terminal(state: Board) -> bool:
        return isinstance(state.get_winner(), str) or state.is_full()

    @staticmethod
    def utility(state: Board, player: str) -> int:
        winner = state.get_winner()
        if winner == player:
            return 1
        elif winner is None:
            return 0
        else:
            return -1

    @staticmethod
    def print_ascii(state: Board) -> None:
        def cell_to_char(val):
            if val is None:
                return '.'
            if isinstance(val, str):
                return val
            return '?'

        lines = []
        for sup_r in range(3):
            for sub_r in range(3):
                row_parts = []
                for sup_c in range(3):
                    if isinstance(state.cells[sup_r][sup_c], list):
                        sub_board = state.cells[sup_r][sup_c]
                        row_parts.append(
                            ''.join(cell_to_char(sub_board[sub_r][sub_c]) for sub_c in range(3))
                        )
                    else:
                        marker = state.cells[sup_r][sup_c]
                        row_parts.append(marker * 3 if marker != 'T' else '===')
                lines.append(' | '.join(row_parts))
            if sup_r < 2:
                lines.append('-' * (3 * 3 + 2 * 3))
        print('\n'.join(lines))