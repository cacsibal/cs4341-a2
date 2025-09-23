# CS 4341 Assignment 2

---

## Overview

Implement a competitive game‐playing agent for **Ultimate Tic‑Tac‑Toe** using **minimax search with α–β pruning**. You will complete the search agent and a heuristic evaluation function, and verify correctness and performance with the provided test harness.

---

## Provided Files

* `board.py` — State representation and game rules for Ultimate Tic‑Tac‑Toe (board layout, move legality, win and tie detection, and turn updates).
* `uttt.py` — Game wrapper exposing a standard search interface (initial state, player to move, action generation, result, terminal test, utility, and ASCII print helper).
* `agent.py` — Templates you must complete: `eval(state, player)`, `Agent.__init__`, and `Agent.search` (minimax with α–β pruning).
* `test.py` — Code for creating four tests (Depth‑1/2/3 and Two‑Agent Play).

---

## Game Mechanics Summary

**Setup:** The board is nine small tic-tac-toe boards arranged in a 3×3 grid (81 total squares). Each small board acts like a space on the big board.

**Goal:** Capture three small boards in a row (row, column, or diagonal) on the big board.

**How turns work:**
1. Two players, X and O. X goes first and may play in any square.
2. After that, the square you choose tells your opponent where to play next: its matching small board on the big grid (e.g., bottom-right square → bottom-right small board).
3. If you are sent to a small board that is already won or full, you may play in any open small board.

**Winning small boards:** Win a small board like normal tic-tac-toe (three in a row). That small board is then marked as yours on the big board and no more moves can be made in it.

**End of game:** The game ends when a player wins three small boards in a row on the big board, or when no legal moves remain (draw).

---

## What You Must Implement

### 1) Heuristic Evaluation

**Function:** `eval(state: Board, player: str) -> float`

* Input: a `Board` state and the perspective player (`'X'` or `'O'`).
* Output: a real value where larger is better for `player`.
* Requirements:

 * Deterministic for identical inputs.
 * Fast enough to allow search at the required depths.
 * May use standard‐library helpers (e.g., `math`) if desired.
 * Design is up to you.

> Note: The test file includes its own reference heuristic for *tests only*. Your own `eval` is still required in your submission file.

### 2) Agent Initialization

**Class:** `Agent`

Implement `__init__(self, player: str, eval, depth_limit: int)` to store:

* `self.player` — the agent’s identity (`'X'` or `'O'`).
* `self.eval` — heuristic function.
* `self.depth_limit` — maximum search depth (plies from the current state).
* Any additional internal fields you need (e.g., a node counter).

### 3) Minimax with α–β Pruning

**Method:** `search(self, state: Board) -> Tuple[float, Tuple[int,int,int,int], int]`

Implement minimax with α–β pruning subject to the following:

* **Player to move:** use `UltimateTicTacToe.to_move(state)` to determine whose turn it is at each node.
* **Terminal test:** use `UltimateTicTacToe.is_terminal(state)`. For terminal nodes, return game‐theoretic utility relative to `self.player` via `UltimateTicTacToe.utility(state, self.player)`.
* **Depth limit:** interpret `depth_limit = d` as searching **d plies** (root at depth 0; root children at depth 1). At the depth limit, evaluate with the provided evaluation function.
* **Actions:** generate children with `UltimateTicTacToe.actions(state)`. Do **not** reorder or sort actions. Iterate exactly in the order provided.
* **Result:** apply actions with `UltimateTicTacToe.result(state, move)`.
* **α–β:** perform standard pruning.
* **Return value:** `(value, move, count)` where:

 * `value` is the minimax value of the move chosen by your agent.
 * `move` is the move chosen by your agent.
 * `count` is the number of nodes evaluated over the entire search (equivalent to the total number of calls of MAX-VALUE or MIN-VALUE).

> **Tie‑breaking:** If multiple moves have the same `value`, return the first encountered in the action iteration.

---

## Running the Tests

1. Place your implementation in the same directory as the provided files.
2. Ensure your file defines `eval`, `Agent`, and the exact method signatures above.
1. Run: `test.py`.
4. `test.py` prints **Expected** and **Actual** values for each test. Your implementation must match exactly.

**Depth tests:** Performs a search with a depth of 1, 2, and 3 using the reference heuristic.

**Two‑Agent Play:** Alternates moves from a fixed position with two agents using the reference heuristic.

---

## Submission Instructions

* Rename your complete `agent.py` to your WPI username, e.g., `ebprihar.py`.
* Upload your file to Canvas.
* Keep your code clean and well commented.
* You may import additional **standard library** modules if helpful for your heuristic.

> **Note on local testing vs. submission:** The supplied `test.py` imports from `agent.py`. For local testing, implement in `agent.py`. For submission, follow the naming rule above.

---

## Grading (100 points)

| Test | Points |
| - | - |
| Depth‑1 Search | 20 |
| Depth‑2 Search | 20 |
| Depth‑3 Search | 20 |
| Two‑Agent Play | 20 |
| Code Cleanliness | 20 |

---

## Rubric

### Test Cases

| Metric | 100% | 0% |
| - | - | - |
| Test Passed | Yes | No |

### Code Cleanliness

| Metric | 100% | 80% | 60% | 40% | 0% |
| - | - | - | - | - | - |
| Structure | Clear, modular functions; no redundancy | Mostly modular; minimal redundancy | Some modularity; some repeated code | Functions are disorganized or too long | No structure; hard to follow |
| Comments | Thorough and helpful throughout | Mostly helpful; a few sections unclear | Sparse or generic comments | Few comments; code is hard to follow | No comments |
| Formatting | Consistent indentation, spacing, naming | Mostly consistent formatting | Minor formatting issues | Several formatting problems | Poor formatting; unreadable |
