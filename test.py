from agent import Agent
from board import Board
from uttt import UltimateTicTacToe

import unittest

def test_eval(state: Board, player: str) -> float:
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

def setup_test_board():
    test_board = Board()
    test_board.cells = [
        [
            [
                [None, 'X', None],
                [None, None, None],
                [None, 'X', 'X']
            ],
            'O',
            [
                ['O', None, None],
                [None, 'X', None],
                [None, 'X', None]
            ]
        ],
        [
            [
                [None, 'O', 'X'],
                ['X', None, None],
                [None, 'O', 'X']
            ],
            [
                ['O', 'X', None],
                ['O', 'O', None],
                ['X', None, None]
            ],
            [
                [None, 'X', None],
                ['O', None, None],
                [None, None, None]
            ]
        ],
        [
            [
                [None, 'O', None],
                [None, 'X', None],
                [None, None, 'O']
            ],
            [
                [None, 'X', None],
                ['X', 'O', None],
                ['X', 'O', 'O']
            ],
            [
                [None, 'X', None],
                ['O', None, 'X'],
                [None, 'X', 'O']
            ]
        ]
    ]
    test_board.active_board = (1, 0)
    test_board.next_player = 'X'
    return test_board


class AgentSearchTests(unittest.TestCase):

    def run_and_compare(self, depth, expected):
        test_board = setup_test_board()
        agent = Agent('X', test_eval, depth)
        value, move, count = agent.search(test_board)
        actual = (value, move, count)
        print(f'\nTest {depth}:')
        print('Expected:', expected)
        print('Actual:  ', actual)
        self.assertEqual(actual, expected)

    def test_depth_1(self):
        self.run_and_compare(1, (9, (1, 0, 1, 2), 5))

    def test_depth_2(self):
        self.run_and_compare(2, (6, (1, 0, 1, 2), 20))

    def test_depth_3(self):
        self.run_and_compare(3, (9, (1, 0, 1, 2), 81))

    def test_two_agents_play_asserted(self):
        agent_x = Agent('X', test_eval, 5)
        agent_o = Agent('O', test_eval, 5)
        board = setup_test_board()

        expected = [
            (11, (1, 0, 1, 2), 1264),
            (-8, (1, 2, 1, 1), 1733),
            (11, (1, 1, 0, 2), 2179),
            (-10, (0, 2, 0, 2), 2104),
        ]

        actual = []
        for _ in range(2):
            value, move, count = agent_x.search(board)
            actual.append((value, move, count))
            board = UltimateTicTacToe.result(board, move)
            if UltimateTicTacToe.is_terminal(board):
                break
            value, move, count = agent_o.search(board)
            actual.append((value, move, count))
            board = UltimateTicTacToe.result(board, move)
            if UltimateTicTacToe.is_terminal(board):
                break
        print(f'\nTest 4:')
        print('Expected:', expected)
        print('Actual:  ', actual)
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
