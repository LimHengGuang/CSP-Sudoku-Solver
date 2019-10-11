class SudokuValidityTester:
    def __init__(self, puzzle):
        self.puzzle = puzzle

    def check_validity(self):
        
        # checking row's validity
        if not self.checking_row_validity(self.puzzle):
            return False

        # checking column's validity
        # Transpose the puzzle first
        transposed_puzzle = [[0 for i in range(9)] for j in range(9)]
        for i, row in enumerate(self.puzzle):
            for j, ele in enumerate(row):
                transposed_puzzle[j][i] = ele
                
        if not self.checking_row_validity(transposed_puzzle):
            return False

        # check each big box's validity
        starting_points = []
        for i in range(0,7,3):
            for j in range(0,7,3):
                starting_points.append((i,j))
                
        for i, j in starting_points:
            ele_set = set()  # initialise a new set to check for uniqueness
            for row in range(i, i + 3):
                for col in range(j, j + 3):
                    if self.puzzle[row][col] in ele_set:
                        return False
                    else:
                        ele_set.add(self.puzzle[row][col])
        return True

    def checking_row_validity(self, puzzle):
        ele_set = set()
        
        # check each row's validity
        for row in self.puzzle:
            for ele in row:
                # 0 signifies empty space, which implies incompleteness.
                if ele in ele_set or ele == 0:
                    return False
                else:
                    ele_set.add(ele)
            # re-initialise a set after each row
            ele_set = set()
        return True

if __name__ == "__main__":
    # ordering the input
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

    tester = SudokuValidtyTester(puzzle)
    print(tester.check_validity())
