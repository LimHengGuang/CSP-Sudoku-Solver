import sys
import os

class SudokuValidityTester:
    def __init__(self, puzzle):
        self.puzzle = puzzle

    def check_validity(self):
        # checking for row and col's validity
        if not self.check_row_col_validity(self.puzzle):
            return False

        # check each big box's validity
        if not self.check_box_validity(self.puzzle):
            return False
        
        return True

    def check_row_col_validity(self, puzzle):
        row_ele_set = set()
        col_ele_set = set()
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] == 0 or puzzle[i][j] in row_ele_set:
                    return False
                if puzzle[j][i] == 0 or puzzle[j][i] in col_ele_set:
                    return False
                else:
                    row_ele_set.add(puzzle[i][j])
                    col_ele_set.add(puzzle[j][i])
            row_ele_set = set()
            col_ele_set = set()
        return True
    
    def check_box_validity(self, puzzle):
        box_coords = [(0,0), (0,3), (0,6), (3,0),\
                      (3,3), (3,6), (6,0), (6,3), (6,6)]
                
        for i, j in box_coords:
            ele_set = set()  # initialise a new set to check for uniqueness
            for row in range(i, i + 3):
                for col in range(j, j + 3):
                    if self.puzzle[row][col] in ele_set:
                        return False
                    else:
                        ele_set.add(self.puzzle[row][col])
        return True

if __name__ == "__main__":
    # ordering the input
    if len(sys.argv) != 2:
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
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

    tester = SudokuValidityTester(puzzle)
    print(tester.check_validity())
