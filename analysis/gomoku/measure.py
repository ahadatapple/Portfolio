"""Measure the Gomoku evaluation against the course bots, with a sample large
enough to mean something. Produces the table on the Gomoku case-study page.

Setup, in one folder:
  - utils.py and kille.py from the course
  - student.py: your helper functions and student_eval, copied out of the
    notebook's heuristic cell, with `from utils import iter_seqs` as line one

Run:
  pip install numpy termcolor tqdm prettytable
  python measure.py            # 200 games per matchup, about 2 to 4 minutes
  python measure.py 500        # more games, tighter ranges

What it checks:
  1. The engine's first move on an empty board.
  2. How many distinct games 20 empty-board games against the hardest bot
     produce. Both players are deterministic, so expect 2.
  3. Win rates over N games per matchup, from an empty board and from the
     course's random starts (16 to 32 random stones on an 8x8 board), with
     95% Wilson confidence intervals.
"""

import math
import random
import sys
from functools import partial
from multiprocessing import Pool

import numpy as np

import kille
from student import student_eval
from utils import Strategy, get_random_board, play_game

BOARD = 8


def one_game(start_stones, difficulty, seed, record_moves=False):
    """Play one game. Returns (student_won, tie, moves)."""
    random.seed(seed)
    board = get_random_board(BOARD, turn_count=start_stones)
    student_first = random.random() <= 0.5
    bot = partial(kille.slider_eval, difficulty=difficulty)
    eval_x, eval_o = (student_eval, bot) if student_first else (bot, student_eval)
    p1, p2 = Strategy("X", eval_x, max_depth=1), Strategy("O", eval_o, max_depth=1)

    moves = []
    if record_moves:
        for p in (p1, p2):
            original = p.get_move

            def recorded(b, _orig=original):
                move = _orig(b)
                moves.append((int(move[0]), int(move[1])))
                return move

            p.get_move = recorded

    winner = play_game(board, p1, p2, suppress_output=True)
    me = "X" if student_first else "O"
    return winner == me, winner is None, tuple(moves)


def matchup(args):
    start, difficulty, seed = args
    stones = random.Random(seed).randint(BOARD**2 // 4, BOARD**2 // 2) if start == "random" else 0
    won, tie, _ = one_game(stones, difficulty, seed)
    return start, difficulty, won, tie


def wilson(wins, n, z=1.96):
    p = wins / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return max(0.0, centre - half), min(1.0, centre + half)


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 200

    empty = np.array([["-"] * BOARD for _ in range(BOARD)])
    print("First move on an empty board:", tuple(int(v) for v in Strategy("X", student_eval, 1).get_move(empty)))

    games = [one_game(0, 1.0, seed, record_moves=True) for seed in range(20)]
    print(
        "Empty board vs hardest bot, 20 games:",
        sum(g[0] for g in games), "wins,",
        len({g[2] for g in games}), "distinct games",
    )

    cells = [("empty", 0.2), ("empty", 0.5), ("random", 0.2), ("random", 0.5), ("random", 1.0)]
    jobs = [(start, diff, 1000 * i + j) for i, (start, diff) in enumerate(cells) for j in range(n)]
    with Pool() as pool:
        results = pool.map(matchup, jobs, chunksize=4)

    print(f"\n{n} games per matchup")
    for start, diff in cells:
        rows = [r for r in results if r[0] == start and r[1] == diff]
        wins = sum(r[2] for r in rows)
        ties = sum(r[3] for r in rows)
        lo, hi = wilson(wins, len(rows))
        print(
            f"  {start:>6} start vs difficulty {diff}: {wins}/{len(rows)} "
            f"({100 * wins / len(rows):.0f}%, 95% CI {100 * lo:.0f}-{100 * hi:.0f}%), {ties} ties"
        )


if __name__ == "__main__":
    main()
