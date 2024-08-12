import numpy as np
import time
import sys
from collections import deque

call_count = 0


class SudokuSolver():

    # load the sudoku puzzle
    def __init__(self, puzzle_file):
        # Read the puzzle from a file with each row in a single line
        self.puzzle = np.array([list(map(int, line.strip())) for line in open(puzzle_file)])
        self.domains = {(i, j): {self.puzzle[i, j]} if self.puzzle[i, j] != 0 else set(
            range(1, 10)) for i in range(9) for j in range(9)}
        self.neighbors = {(x, y): set((i, j) for i in range(9) for j in range(9) if (x == i or y == j or (
            x // 3 == i // 3 and y // 3 == j // 3)) and (x, y) != (i, j)) for x in range(9) for y in range(9)}

    def print_board(self):
        for row in self.puzzle:
            print(" ".join(str(cell) if cell != 0 else '.' for cell in row))
        print()

    def solve(self):
        assignment = dict()
        for i in range(9):
            for j in range(9):
                if self.puzzle[i, j] != 0:
                    assignment[(i, j)] = self.puzzle[i, j]
        '''
        self.ac3()
        '''
        return self.backtrack(assignment)

    # Make x arc consistent with y
    '''
    def revise(self, x, y):
        if y not in self.neighbors[x]:
            return False
        else:
            inconsistent = set()
            revised = False
            for x_val in self.domains[x]:
                consistent = False
                for y_val in self.domains[y]:
                    if y_val != x_val:
                        consistent = True
                        break
                if not consistent:
                    revised = True
                    inconsistent.add(x_val)

            self.domains[x] = self.domains[x] - inconsistent

        return revised
        '''
    '''
    def ac3(self, arcs=None):
        if arcs is None:
            arcs = deque((x, y) for x in self.domains for y in self.domains[x])

        while arcs:
            x, y = arcs.popleft()
            if self.revise(x, y):
                if not self.domains[x]:
                    return False
                arcs.extend((z, x) for z in self.neighbors[x] if z != y)
        return True
    '''

    def consistent(self, cell, value, assignment):
        for y in self.neighbors[cell]:
            if y in assignment and value == assignment[y]:
                return False
        return True

    def select_unassigned_cell(self, assignment):
        return min((cell for cell in self.domains if cell not in assignment), key=lambda cell: len(self.domains[cell]))

    def order_domain_values(self, cell, assignment):
        return sorted(self.domains[cell], key=lambda value: sum(value in self.domains[neighbor] for neighbor in self.neighbors[cell] if neighbor not in assignment))

    def backtrack(self, assignment):
        global call_count
        call_count += 1
        if len(assignment) == len(self.domains):
            return assignment

        cell = self.select_unassigned_cell(assignment)
        for value in self.order_domain_values(cell, assignment):
            if self.consistent(cell, value, assignment):
                assignment[cell] = value
                '''
                inferences = self.inference(cell, assignment)
                if inferences:
                    assignment.update(inferences)
                '''
                result = self.backtrack(assignment)
                if result:
                    return result
                '''
                if inferences:
                    for inference in inferences:
                        assignment.pop(inference)
                '''
                assignment.pop(cell)

        return None
    '''
    def inference(self, cell, assignment):
        inferences = {}
        queue = deque((neighbor, cell) for neighbor in self.neighbors[cell])

        if self.ac3(queue):
            for c in self.domains:
                if c not in assignment and len(self.domains[c]) == 1:
                    inferences[c] = list(self.domains[c])[0]
            return inferences
        return None
    '''


def main():

    if len(sys.argv) != 2:
        sys.exit("Usage: python sudoku.py sudoku.txt")

    sudoku = SudokuSolver(sys.argv[1])
    start = time.time()
    sudoku.print_board()
    assignment = sudoku.solve()

    if assignment is None:
        print("No solution.")
    else:
        end = time.time()
        length = end - start
        print("Solved")
        print("It took", length, "seconds!")
        print(f"Number of recursive calls: {call_count}")
        for i in range(9):
            for j in range(9):
                print(assignment[(i, j)], end=" ")
            print()


if __name__ == "__main__":
    main()
