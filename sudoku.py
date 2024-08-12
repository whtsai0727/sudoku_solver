import sys
import time

call_count = 0  # Global variable to count the number of recursive calls

def print_board(board):
    """Helper function to print the board in a user-friendly format."""
    for row in board:
        print(" ".join(str(cell) if cell != 0 else '.' for cell in row))
    print()

def is_valid(board, row, col, num):
    """Check if it's valid to place the number 'num' in the position board[row][col]."""
    # Check the row and column
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    # Check the 3x3 sub-grid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False

    return True

def find_empty_location(board):
    """Find the empty location on the board with the minimum remaining values."""
    min_possibilities = float('inf')
    best_row, best_col = -1, -1

    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                # Count the number of possibilities for this cell
                possibilities = sum(is_valid(board, row, col, num) for num in range(1, 10))
                if possibilities < min_possibilities:
                    min_possibilities = possibilities
                    best_row, best_col = row, col
                    if min_possibilities == 1:
                        return best_row, best_col

    return best_row, best_col

def get_least_constraining_values(board, row, col):
    """Order possible values by least constraining value heuristic, considering only neighbors."""
    constraints = {}
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            count = 0
            # Consider only the neighbors of the cell
            for r, c in get_neighbors(row, col):
                if board[r][c] == 0 and is_valid(board, r, c, num):
                    count += 1
            constraints[num] = count
    return sorted(constraints, key=constraints.get)

def get_neighbors(row, col):
    """Return the coordinates of neighbors of a given cell."""
    neighbors = []
    for r in range(9):
        for c in range(9):
            if (r == row or c == col or (row // 3 == r // 3 and col // 3 == c // 3)) and (r, c) != (row, col):
                neighbors.append((r, c))
    return neighbors

def solve_sudoku(board):
    """Solve the Sudoku puzzle using backtracking with heuristics."""
    global call_count
    call_count += 1

    row, col = find_empty_location(board)
    if row == -1 and col == -1:
        return True

    for num in get_least_constraining_values(board, row, col):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0

    return False

def read_board_from_file(filename):
    """Read the Sudoku board from a text file with no spaces between numbers."""
    board = []
    with open(filename, 'r') as file:
        for line in file:
            # Convert each character to an integer and append the row to the board
            board.append([int(char) for char in line.strip()])
    return board

def main():
    if len(sys.argv) != 2:
        print("Usage: python sudoku_solver.py <sudoku_file.txt>")
        sys.exit(1)

    filename = sys.argv[1]
    board = read_board_from_file(filename)

    print("Original board:")
    print_board(board)

    start_time = time.time()

    if solve_sudoku(board):
        print("Solved board:")
        print_board(board)
    else:
        print("No solution exists.")

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Number of recursive calls: {call_count}")
    print(f"Solving time: {elapsed_time:.4f} seconds")

if __name__ == "__main__":
    main()
