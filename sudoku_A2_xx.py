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
        self.initialise_sets()
        self.init_arc_consistency()

    # initial removal of domains using arc consistency algorithm
    def init_arc_consistency(self):
        for i, row in enumerate(self.puzzle):
            for j, ele in enumerate(row):
                if ele != 0:
                    self.row_set[i].remove(ele)
                    self.col_set[j].remove(ele)

                    top_left_i = i // 3
                    top_left_j = j // 3
                    self.box_set[(top_left_i, top_left_j)].remove(ele)

    def initialise_sets(self):
        # initialising box_set
        for coord in self.box_coords:
                box_set[coord] = set([1,2,3,4,5,6,7,8,9])
        for i in range(9):
            row_set[i] = set([1,2,3,4,5,6,7,8,9])
            col_set[i] = set([1,2,3,4,5,6,7,8,9])
                        
    def form_row_set(self, puzzle, set_dic):
        for i, row in enumerate(puzzle):
            set_dic[i] = set()
            for ele in row:
                if ele != 0:
                    set_dic[i].add(ele)

    def form_col_set(self, puzzle, set_dic):
        for i in range(9):
            for j in range(9):
                
        
    def transpose_puzzle(self, puzzle):
        # Transpose the puzzle first
        transposed_puzzle = [[0 for i in range(9)] for j in range(9)]
        for i, row in enumerate(puzzle):
            for j, ele in enumerate(row):
                transposed_puzzle[j][i] = ele
        return transposed_puzzle

    def solve(self):
        # Main idea
        
        # don't print anything here. just resturn the answer
        # self.ans is a list of lists
        return self.ans

    
    # check whether element is legal within the box surrounding the cell_ij
    def check_in_box_set(self, ele, i, j):
        top_left_i = i // 3
        top_left_j = j // 3
        if item in self.box_set[(top_left_i, top_left_j)]:
            return True
        else:
            return False

    # checks for common elements between row_set, col_set and box_set
    def union_cell(self, coord):
        ele_set = set()
        for item in self.row_set[coord]:
            if item in self.col_set[coord] and self.check_in_box_set(item, coord[0], coord[1]):
                ele_set.add(item)
        return ele_set

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
