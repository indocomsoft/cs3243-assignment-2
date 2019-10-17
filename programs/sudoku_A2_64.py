"""
Sudoku solver
"""

import sys
import copy
from collections import deque

DOMAIN = set(range(1, 10))
SAME_SQUARE = []
for square_num in xrange(9):
    top_left_r = 0 + square_num // 3 * 3
    top_left_c = 0 + square_num % 3 * 3
    SAME_SQUARE.append(set((top_left_r + r, top_left_c + c) for c in xrange(3)
                 for r in xrange(3)))

class Sudoku(object):
    def __init__(self, puzzle, **kwargs):
        if kwargs:
            self.ans = kwargs["ans"]
            self.possible = kwargs["possible"]
            return

        # Faster than copy.deepcopy because we know puzzle is not recursive
        self.ans = [row[:] for row in puzzle]
        n = len(puzzle)
        rows = [set() for _ in xrange(n)]
        cols = [set() for _ in xrange(n)]
        squares = [set() for _ in xrange(n)]

        for r in xrange(n):
            for c in xrange(n):
                number = puzzle[r][c]
                if number:
                    rows[r].add(number)
                    cols[c].add(number)
                    squares[self.get_square_num(r, c)].add(number)

        self.possible = [[set() for c in xrange(len(puzzle[r]))]
                         for r in xrange(len(puzzle))]
        self.queue = deque()
        self.in_queue = set()
        # Initialise possibilities
        for r in xrange(n):
            for c in xrange(n):
                number = puzzle[r][c]
                if number:
                    self.possible[r][c] = set([number])
                else:
                    self.possible[r][c] = DOMAIN - \
                        rows[r] - \
                        cols[c] - \
                        squares[self.get_square_num(r, c)]
                    if len(self.possible[r][c]) == 1:
                        (v, ) = self.possible[r][c]
                        self.queue.append((r, c, v))
                        self.in_queue.add((r, c))

    def solve(self):
        result, max_depth, max_branch = self.recurse_solve(0)
        print("max_depth = {0}, max_branch = {1}".format(
            max_depth, max_branch))
        return result

    def recurse_solve(self, depth):
        max_depth = depth
        max_branch = cur_branch = 0
        while self.queue:
            r, c, v = self.queue.popleft()
            self.in_queue.remove((r, c))
            self.ans[r][c] = v
            self.possible[r][c] = set([v])
            recheck_cells = set((r, i) for i in xrange(len(self.ans))) | \
                set((i, c) for i in xrange(len(self.ans))) | \
                SAME_SQUARE[self.get_square_num(r, c)]
            recheck_cells.remove((r, c))
            for r, c in recheck_cells:
                self.possible[r][c].discard(v)
                if not self.possible[r][c]:
                    return (False, max_depth, max_branch)
                if len(self.possible[r][c]) == 1 and \
                        self.ans[r][c] == 0 and \
                        (r, c) not in self.in_queue:
                    (v_, ) = self.possible[r][c]
                    self.queue.append((r, c, v_))
                    self.in_queue.add((r, c))

        # If already complete
        if all(0 not in row for row in self.ans):
            return (self.ans, max_depth, max_branch)

        r, c = self.get_most_constrained()
        for v in self.possible[r][c]:
            cur_branch += 1
            max_branch = max(cur_branch, max_branch)

            other = self.copy()

            other.queue = deque([(r, c, v)])
            other.in_queue = set([(r, c)])
            result, d, b = other.recurse_solve(depth + 1)
            max_depth = max(d, max_depth)
            max_branch = max(b, max_branch)
            if result:
                return (result, max_depth, max_branch)
        return (False, max_depth, max_branch)

    def copy(self):
        return Sudoku(None,
                      ans=[row[:] for row in self.ans],
                      possible=[[set(cell) for cell in row]
                                for row in self.possible])

    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY
    def get_square_num(self, r, c):
        return 3 * (r // 3) + c // 3

    def get_most_constrained(self):
        candidate = ((), 9)
        n = len(self.ans)
        for r in xrange(n):
            for c in xrange(n):
                cur_len = len(self.possible[r][c])
                if 1 < cur_len < candidate[1]:
                    candidate = ((r, c), cur_len)
        return candidate[0]


if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print("\nUsage: python sudoku_A2_xx.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print("\nUsage: python sudoku_A2_xx.py input.txt output.txt\n")
        raise IOError("Input file not found!")

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")
