import sys
import copy

class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists
        self.row_set = {}
        self.col_set = {}
        self.box_set = {}

        # initialising box top left coordinates
        self.box_coords = [(0,0), (0,3), (0,6), (3,0),\
                           (3,3), (3,6), (6,0), (6,3), (6,6)]

        # setting up all the contraints
        self.initialise_row_set()
    
    def initialise_row_set(self):
        # forming row_set
        self.form_set(self.puzzle, self.row_set)
        
        # forming col_set
        transposed_puzzle = self.transpose_puzzle(self.puzzle)
        self.form_set(transposed_puzzle, self.col_set)

        # forming box_set
        self.form_box_set(self.puzzle, self.box_set)
                               
    def form_box_set(self, puzzle, set_dic):
        for coord in self.box_coords:
            i, j = coord
            set_dic[coord] = set()
            for row in range(i, i + 3):
                for col in range(j, j + 3):
                    if self.puzzle[row][col] != 0:
                        set_dic[coord].add(self.puzzle[row][col])
                        
    def form_set(self, puzzle, set_dic):
        for i, row in enumerate(puzzle):
            set_dic[i] = set()
            for ele in row:
                if ele != 0:
                    set_dic[i].add(ele)
        
    def transpose_puzzle(self, puzzle):
        # Transpose the puzzle first
        transposed_puzzle = [[0 for i in range(9)] for j in range(9)]
        for i, row in enumerate(puzzle):
            for j, ele in enumerate(row):
                transposed_puzzle[j][i] = ele
        return transposed_puzzle

    def solve(self):
        #TODO: Your code here

        # don't print anything here. just resturn the answer
        # self.ans is a list of lists
        return self.ans

    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY

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
