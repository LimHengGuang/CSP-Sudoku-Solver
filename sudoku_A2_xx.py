import sys
import copy

class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists

        # 2-D table of bool
        # False if the value hasn't been fixed. True otherwise
        self.puzzle_bool = [[False for i in range(len(puzzle[0]))] \
                            for i in range(len(puzzle))]
        
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
                    # remove these elements from the domain
                    self.manage_domains(i, j, ele, False)


    def initialise_sets(self):
        # initialising box_set
        for coord in self.box_coords:
                box_set[coord] = set([1,2,3,4,5,6,7,8,9])
        for i in range(9):
            row_set[i] = set([1,2,3,4,5,6,7,8,9])
            col_set[i] = set([1,2,3,4,5,6,7,8,9])
            
    def manage_domains(self, i, j, ele, to_add):
        '''
        Takes in coordinates i, j
        and the element to add/remove
        If to_add is True, add ele into domains
        Otherwise, remove ele from domains
        '''
        row_set = self.row_set[i]
        col_set = self.col_set[j]

        top_left_i = i // 3
        top_left_j = j // 3
        box_set = self.box_set[(top_left_i, top_left_j)]
        
        if to_add:
            row_set.add(ele)
            col_set.add(ele)
            box_set.add(ele)
        else:
            row_set.remove(ele)
            col_set.remove(ele)
            box_set.remove(ele)
        
    def solve(self):
        # Main idea
        
        # don't print anything here. just resturn the answer
        # self.ans is a list of lists

        self.solver_helper(self.ans)
        
        return self.ans

    # returns True if it manages to solve
    # returns False if it encounters an empty domain
    def solver_helper(self, puzzle):
        # find cell with smallest domain
        # then run a for-loop and continue to recurse with a value fixed
        cell_set, coord = self.find_most_constrained_cell(puzzle, puzzle_bool)
        if len(cell_set) == 0:
            return False
        else:
            for ele in cell_set:
                i, j = coord
                puzzle[i][j] = ele
                manage_domains(i, j, ele, False)
                if not self.solver_helper(puzzle):
                    # if this assignment does not work
                    # then backtrack and undo the assignment
                    puzzle[i][j] = 0
                    manage_domains(i, j, ele, True)
                    continue
                else:
                    return True
            return False
        
    # using most constrained variable heuristic
    def find_most_constrained_cell(self, puzzle, puzzle_bool):
        min_set_size = float('inf')
        min_set = None
        min_set_coord = None
        
        for i, row in enumerate(puzzle):
            for j, ele in enumerate(row):
                # if the variable is not fixed yet
                if puzzle[i][j] != 0:
                    coord = (i, j)
                    cell_set = self.get_cell_domain(coord)
                    cell_set_size = len(cell_set)

                    # if you found a cell with empty domain
                    # return it immediately
                    if cell_set_size == 0:
                        return (cell_set, coord)
                    
                    if cell_set_size < min_set_size:
                        min_set_size = cell_set_size
                        min_set = cell_set
                        min_set_coord = coord
        return (min_set, min_set_coord)

    
    # check whether element is legal within the box surrounding the cell_ij
    def check_in_box_set(self, ele, i, j):
        top_left_i = i // 3
        top_left_j = j // 3
        if item in self.box_set[(top_left_i, top_left_j)]:
            return True
        else:
            return False

    # checks for common elements between row_set, col_set and box_set
    def get_cell_domain(self, coord):
        '''
        Takes in the coordinate of a cell
        Returns the domain of the cell,
        which is the intersection between the 3 domains: row_set, col_set, box_set 
        '''
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
