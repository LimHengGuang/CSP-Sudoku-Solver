import sys
import copy

class Sudoku(object):
    def __init__(self, puzzle):
        self.puzzle = puzzle # models the sudoku as a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists

        # initialising box top left coordinates
        self.box_coords = [(0,0), (0,3), (0,6), (3,0),\
                           (3,3), (3,6), (6,0), (6,3), (6,6)]

        # Since domain set of each cell (variable) is unique among
        # row, col and box, we can represent the domains by rows, cols and boxes
        # stores the domain of each row, key: row_number, value: domain_set
        self.row_set = {}
        # stores the domain of each col, key: col_number, value: domain_set
        self.col_set = {}
        # stores the domain of each box, key: box_top_left_coord, value: domain_set
        self.box_set = {}

        # setting up the contraints
        self.initialise_sets()
        self.init_arc_consistency()

    def initialise_sets(self):
        '''initialising domains of rows, cols, and boxes'''
        for coord in self.box_coords:
                self.box_set[coord] = set([1,2,3,4,5,6,7,8,9])
        for i in range(9):
            self.row_set[i] = set([1,2,3,4,5,6,7,8,9])
            self.col_set[i] = set([1,2,3,4,5,6,7,8,9])
            
    def init_arc_consistency(self):
        '''initial removal of domains using arc consistency algorithm'''
        for i, row in enumerate(self.puzzle):
            for j, ele in enumerate(row):
                # only care about non-empty spaces
                if ele != 0:
                    # remove these elements from the domain
                    self.manage_domains(i, j, ele, False)
            
    def manage_domains(self, i, j, ele, to_add):
        '''
        Takes in coordinates i, j
        and the element to add/remove
        If to_add is True, add ele into domains
        Otherwise, remove ele from domains
        '''
        row_set = self.row_set[i]
        col_set = self.col_set[j]

        top_left_i = i - (i % 3)
        top_left_j = j - (j % 3)
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
        '''
        Pre-condition: the initial puzzle given must be valid and solvable
        '''
        self.solver_helper(self.ans)
        return self.ans

    def solver_helper(self, puzzle):
        '''
        Takes a partially/fully solved sudoku puzzle as input
        Returns True if it can be solved
        Returns False if it cannot be solved (one of the cell domains is empty)
        '''
        
        # find cell with smallest domain (most constrained variable heuristic)
        cell_set, coord = self.find_most_constrained_cell(puzzle)
        #print(cell_set, coord)

        # if puzzle is completed, then return True
        if cell_set is None:
            return True
        
        # if there is an empty domain, return False
        if len(cell_set) == 0:
            return False
        else:
            for ele in cell_set:
                i, j = coord
                puzzle[i][j] = ele
                self.manage_domains(i, j, ele, False)  # remove ele from domains
                if not self.solver_helper(puzzle):
                    # if this assignment does not work
                    # then backtrack and undo the assignment
                    puzzle[i][j] = 0
                    self.manage_domains(i, j, ele, True) # add ele back to domains
                else:
                    return True
            return False
    
    def find_most_constrained_cell(self, puzzle):
        '''
        This is a HEURISTIC function.
        Finds the cell with the smallest domain
        And return a tuple of (cell's domain, cell's coordinate)
        '''
        min_set_size = float('inf')
        min_set = None
        min_set_coord = None
        
        for i, row in enumerate(puzzle):
            for j, ele in enumerate(row):
                # if the variable has not been fixed yet (0 signifies empty cell)
                if puzzle[i][j] == 0:
                    coord = (i, j)
                    cell_set = self.get_cell_domain(i, j)
                    cell_set_size = len(cell_set)

                    # if you found a cell with empty domain
                    # stop the search and return it immediately
                    if cell_set_size == 0:
                        return (cell_set, coord)
                    
                    if cell_set_size < min_set_size:
                        min_set_size = cell_set_size
                        min_set = cell_set
                        min_set_coord = coord
                        
        # min_set is None if all cells in puzzle is filled up
        return (min_set, min_set_coord)

    def in_box_set(self, ele, i, j):
        '''
        Takes in element and coordinate
        If the element is within box domain, return True
        Otherwise, return False
        '''
        top_left_i = i - (i % 3)
        top_left_j = j - (j % 3)
        if ele in self.box_set[(top_left_i, top_left_j)]:
            return True
        else:
            return False

    def get_cell_domain(self, i, j):
        '''
        Takes in the coordinate of a cell
        Returns the domain of the cell, equivalent to the intersection
        between the 3 domains: row_set, col_set, box_set 
        '''
        ele_set = set()
        for ele in self.row_set[i]:
            if ele in self.col_set[j] and self.in_box_set(ele, i, j):
                ele_set.add(ele)
        return ele_set


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
