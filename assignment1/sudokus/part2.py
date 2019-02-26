"""
    Source code created for DVA340 - Artificiell Intelligens.
    Code writer:
        - Clara Torre García-Barredo.
    Code created on February 2019.
"""

import time
start = time.time()
from copy import deepcopy

def read_file():
    input_file  = open("assignment1/sudokus/assignment1sudoku.txt", "r")
    input_file.readline()
    input_file.readline()
    number_of_sudokus = int(input_file.readline().split()[1])
    # Number of sudokus obtained.
    sudokus = [] #type: list
    while len(sudokus) < number_of_sudokus:
        input_file.readline()
        sudoku = [] #type: list
        while len(sudoku) < 9:
            list_chars = list(input_file.readline())
            list_ints = []
            for i in range (0,9):
                # I cast the characters gotten from the txt file into ints to work better.
                list_ints.append(int(list_chars[i]))
            sudoku.append(list_ints)
        # Sudoku obtained.
        sudokus.append(sudoku)
    # File read.
    return sudokus

def check_possibilities(sudoku, row_index, col_index):
    possibilities = [1, 2, 3, 4, 5, 6, 7, 8, 9] #type: list
    # I check the row first.
    for i in range (1,10):
        if i in sudoku[row_index]:
            possibilities.remove(i)
    # I check the column second.
    for i in range (0,9):
        for j in range (1,10):
            if j == sudoku[i][col_index] and j in possibilities:
                possibilities.remove(j)
    # I check the 3x3 square last.
    if row_index in [0, 1, 2]:
        m = 0
    elif row_index in [3, 4, 5]:
        m = 3
    else: 
        m = 6
    if col_index in [0, 1, 2]:
        n = 0
    elif col_index in [3, 4, 5]:
        n = 3
    else: 
        n = 6
    for j in range(0,3): #j refers to rows
        for k in range(0,3): #k refers to columns
            for i in range(1,10):
                if i == sudoku[m+j][n+k] and i in possibilities:
                    possibilities.remove(i)
    return possibilities

def find_zero_least_possiblities(sudoku, possibilities):
    min_row_index = 10
    min_col_index = 10
    min_number = 10
    row_index = 0
    for row in sudoku:
        col_index = 0
        for cell in range (0, 9):
            if row[cell] == 0:
                if len(possibilities[row_index][col_index]) < min_number: 
                    min_row_index = row_index
                    min_col_index = col_index
                    min_number = len(possibilities[row_index][col_index])
            col_index += 1
        row_index += 1
    return min_row_index, min_col_index

def solve_sudoku(sudoku):
    stack = [] #type: list
    possibilities = [] #type: list
    for row_index in range(0,9):
        possibilities_row = [] #type: list
        for col_index in range(0,9):
            if sudoku[row_index][col_index] == 0:
                possibilities_row.append(check_possibilities(sudoku, row_index, col_index))
            else: 
                possibilities_row.append([])
        possibilities.append(possibilities_row)
    stack.append(sudoku)
    while len(stack) > 0:
        current_sudoku = stack.pop()
        row_index, col_index = find_zero_least_possiblities(current_sudoku, possibilities)
        if row_index == 10 or col_index == 10:
            break
        current_possibilities = check_possibilities(current_sudoku, row_index, col_index)
        for i in current_possibilities:
            if len(current_possibilities) == 1:
                current_sudoku[row_index][col_index] = i
                stack.append(current_sudoku)
            else:
                sudoku_possible = deepcopy(current_sudoku)
                sudoku_possible[row_index][col_index] = i
                stack.append(sudoku_possible)
    return current_sudoku
# Main function.

sudokus = read_file()
solution = [] #type: list
for sudoku in sudokus:
    solution.append(solve_sudoku(sudoku))
for sudoku in solution:
    for row in sudoku:
        print(row)
    print()

print("Execution time:")
end = time.time()
print(end - start)