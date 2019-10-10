import sys
import copy
from collections import deque

DOMAIN = set(range(1,10))

class Sudoku(object):
    def __init__(self, puzzle):
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists
        self.rows = [set() for i in xrange(len(puzzle))]
        self.cols = [set() for i in xrange(len(puzzle))]
        self.squares = [set() for i in xrange(len(puzzle))]
        for r in xrange(len(puzzle)):
            for c in xrange(len(puzzle[r])):
                number = puzzle[r][c]
                if number != 0:
                    self.rows[r].add(number)
                    self.cols[c].add(number)
                    self.squares[self.get_square_num(r, c)].add(number)

        self.possible = [[set() for c in xrange(len(puzzle[r]))] for r in xrange(len(puzzle))]
        self.queue = deque([])
        # Initialise possibilities
        for r in xrange(len(puzzle)):
            for c in xrange(len(puzzle[r])):
                number = puzzle[r][c]
                if number != 0:
                    self.possible[r][c] = {number}
                else:
                    self.possible[r][c] = DOMAIN - \
                        self.rows[r] - \
                        self.cols[c] - \
                        self.squares[self.get_square_num(r, c)]
                    if len(self.possible[r][c]) == 1:
                        self.queue.append((r, c, self.possible[r][c].copy().pop()))

    def solve(self):
        while self.queue:
            r, c, v = self.queue.popleft()
            if self.ans[r][c] == v:
                continue
            self.ans[r][c] = v
            self.rows[r].add(v)
            self.cols[c].add(v)
            self.squares[self.get_square_num(r, c)].add(v)
            self.possible[r][c] = { v }
            recheck_cells = {(r, i) for i in xrange(len(self.puzzle))} | \
                {(i, c) for i in xrange(len(self.puzzle))} | \
                self.same_square(r, c)
            recheck_cells.remove((r, c))
            for r, c in recheck_cells:
                self.possible[r][c].discard(v)
                if len(self.possible[r][c]) == 0:
                    return False
                if len(self.possible[r][c]) == 1 and self.ans[r][c] == 0:
                    self.queue.append((r, c, self.possible[r][c].copy().pop()))

        if self.is_complete():
            return self.ans

        r, c = self.get_most_constrained()
        for v in self.possible[r][c]:
            other = copy.deepcopy(self)
            other.queue.append((r, c, v))
            result = other.solve()
            if result:
                return result
        return False

    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY
    def get_square_num(self, r, c):
        return 3 * (r // 3) + c // 3

    def same_square(self, r, c):
        square_num = self.get_square_num(r, c)
        top_left_r = 0 + square_num // 3 * 3
        top_left_c = 0 + square_num % 3 * 3
        return set((top_left_r + r, top_left_c + c) for c in xrange(3) for r in xrange(3))

    def is_complete(self):
        return all(map(lambda row: 0 not in row, self.ans))

    def get_most_constrained(self):
        candidate = ((0, 0), 9)
        for r in xrange(len(self.puzzle)):
            for c in xrange(len(self.puzzle)):
                cur_len = len(self.possible[r][c])
                if 1 < cur_len < candidate[1]:
                    candidate = ((r, c), cur_len)
        return candidate[0]

if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print ("\nUsage: python sudoku_A2_xx.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print ("\nUsage: python sudoku_A2_xx.py input.txt output.txt\n")
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
