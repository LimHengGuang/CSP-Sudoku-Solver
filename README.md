# CSP Sudoku Solver
The CSP Sudoku Solver takes as input a well-formed sudoku puzzle (a puzzle that can yield a unique solved puzzle), models it as a Constraint Satisfaction Problem (CSP), and outputs the uniquely solved sudoku puzzle.

Code was written with the intention of revising and implementing techniques covered in Introduction to Artificial Intelligence (CS3243). Techniques used in the script involves Arc-consistency Propagation, Forward Checking, and Minimum Remaining Value (MRV) heuristic.

## Usage
Written with the intention to be run using ```Python 2.6```. However, you may run the scripts with ```Python 3.7```, no changes required.

#### To run Sudoku Solver
```python
python sudoku_solver.py input_file output_file
```

#### Input format
Takes in a 9x9 matrix, with each digit separated by a spacebar. 0 represents an unfilled cell. Check out ```./sample_inputs``` for more details.

#### Output format
Outputs a 9x9 matrix that represents a solved state of the input sudoku puzzle. Do note, however, that the uniqueness of the output is dependent on whether or not the sudoku puzzle is well-formed.


## Algorithm Design and Rationale
In the CSP Sudoku Solver, <u>Arc consistency</u>, <u>MRV Heuristic</u>, and <u>backtracking with forward checking</u> was used. The intuition behind these techniques is to increase the likelihood of leaning more towards the best case scenario, achieving lesser guesses and lesser backtracking per cell to reduce the runtime required.

Before diving into the techniques used, let us draw the correlation between intuition and AI techniques, by thinking of how a rational human would normally approach to solve a sudoku.
1. Eliminate possibilities of values in cells related to the pre-filled cells (Maintaining Arc Consistency).
2. Pick a cell with the smallest number of remaining legal values (MRV Heuristic), and start guessing the value for this cell.
3. Each time you pick one value, strike-off the value away from related cells, so you don't violate any sudoku rules. (Forward Checking).
4. When you realise there's a cell with no more legal values, you know you definitely did something wrong previously...so, erase your previous guess(es) (Backtracking).

#### 1. Arc consistency
Due to the uniqueness of values in each row, column and 3 × 3 boxes, we can just simply keep track of the domains of each column, each row and each 3×3 box. Then, the domain of each cell (i,j) is the intersection between the domain of row i, column j and the 3 × 3 box that this cell is contained in.

Arc consistency is first established on the partially solved input to reduce domains of each cell, in order to filter out redundant traversal of subtrees that would eventually violate certain constraints. This process removes the value from the domains of the row, column and box in which the filled cell is in, which then establishes arc consistency with cells that shares the same row, column and box. E.g. If you were to let cell at coordinate (1,2) take up the value 4, then this removes 4 from domain of row 1, 4 from domain of column 2, and 4 from domain of the 3×3 box the cell (1,2) is in.
#### 2. MRV Heuristic
With MRV heuristic, we systematically choose a variable with the smallest domain. In contrast to randomly choosing a domain to work on, a smaller domain means we have a higher probability of ”guessing” a correct variable. Even if we guessed it wrongly in the first few tries, we are more likely to arrive at a correct value assignment with fewer backtracks, hence spent lesser time traversing invalid recursion trees.

#### 3. Backtracking with Forward Checking
With forward checking, the domains of the other variables are updated and checked for emptiness each time a variable is assigned. If this check indicates an empty domain, we can then ascertain that we have wrongly assigned some variable(s) previously, and then immediately backtrack. Like arc-consistency, unnecessary domains are removed along the way to save up time from meaningless exploration of subtrees that are guaranteed to have failed assignments.
