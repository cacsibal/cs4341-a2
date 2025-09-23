import copy
from typing import List, Optional, Tuple

class Board:
    def __init__(self) -> None:
        self.cells = [
            [
                [
                    [
                        None for _ in range(3)
                    ] for _ in range(3)
                ] for _ in range(3)
            ] for _ in range(3)
        ]
        self.active_board = None
        self.next_player = 'X'

    def place(self, sup_r: int, sup_c: int, sub_r: int, sub_c: int) -> None:
        '''
            Place a move and update board state.
        '''
        # Place the next player's piece.
        if self.cells[sup_r][sup_c][sub_r][sub_c] is not None:
            raise ValueError(f'Cell [{sup_r}, {sup_c}, {sub_r}, {sub_c}] is already taken')
        self.cells[sup_r][sup_c][sub_r][sub_c] = self.next_player

        # Check and update the sub-board's win-state.
        if self.is_sub_win(sup_r, sup_c):
            self.cells[sup_r][sup_c] = self.next_player
        elif self.is_sub_full(sup_r, sup_c):
            self.cells[sup_r][sup_c] = 'T'

        # Set the next active board.
        if isinstance(self.cells[sub_r][sub_c], list):
            self.active_board = (sub_r, sub_c)
        else:
            self.active_board = None

        # Switch the next player.
        self.next_player = 'O' if self.next_player == 'X' else 'X'

    def get_legal_moves(self) -> List[Tuple[int, int, int, int]]:
        '''
            Return list of legal moves: (super-row, super-column, sub-row, sub-column).
        '''
        moves = []
        for sup_r in range(3):
            for sup_c in range(3):
                is_target_board = self.active_board == (sup_r, sup_c)
                is_any_open_board = self.active_board is None and isinstance(self.cells[sup_r][sup_c], list)
                if is_target_board or is_any_open_board:
                    for sub_r in range(3):
                        for sub_c in range(3):
                            if self.cells[sup_r][sup_c][sub_r][sub_c] is None:
                                moves.append((sup_r, sup_c, sub_r, sub_c))
        return moves

    def is_sub_win(self, sup_r: int, sup_c: int) -> bool:
        '''
            Check if a sub-board is won.
        '''
        b = self.cells[sup_r][sup_c]
        r_lines = [b[r] for r in range(3)]
        c_lines = [[b[r][c] for r in range(3)] for c in range(3)]
        d_lines = [[b[i][i] for i in range(3)], [b[i][2 - i] for i in range(3)]]
        for line in r_lines + c_lines + d_lines:
            if line[0] is not None and line.count(line[0]) == 3:
                return True
        return False

    def is_sub_full(self, sup_r: int, sup_c: int) -> bool:
        '''
            Check if a sub-board is full.
        '''
        return all(
            self.cells[sup_r][sup_c][r][c] is not None for r in range(3) for c in range(3)
        )

    def get_winner(self) -> Optional[str]:
        '''
            Check if the super-board is won.
        '''
        b = self.cells
        r_lines = [b[r] for r in range(3)]
        c_lines = [[b[r][c] for r in range(3)] for c in range(3)]
        d_lines = [[b[i][i] for i in range(3)], [b[i][2 - i] for i in range(3)]]
        for line in r_lines + c_lines + d_lines:
            if isinstance(line[0], str) and line[0] != 'T' and line.count(line[0]) == 3:
                return line[0]
        return None

    def is_full(self) -> bool:
        '''
            Check if the super-board is full.
        '''
        return all(
            isinstance(self.cells[r][c], str) for r in range(3) for c in range(3)
        )

    def copy(self) -> 'Board':
        '''
            Return a deep copy of the board.
        '''
        return copy.deepcopy(self)

    def print(self) -> None:
        print(self.cells, self.active_board, self.next_player)
