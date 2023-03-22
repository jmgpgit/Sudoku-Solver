from itertools import product

class Sudoku:
    def __init__(self):
        self.sudoku = {(i+1,j+1) : [k+1 for k in range(9)] for i in range(9) for j in range(9)}
    
    def __repr__(self):
        return str(self.sudoku)
    
    def fill(self, x, y, val):
        self.sudoku[(x,y)] = [val]
        
    def _reduce_3x3(self, x, y):
        solved = set()
        for i,j in product(range(3*x-3, 3*x), range(3*y-3, 3*y)):
            if len(self.sudoku[(i+1,j+1)]) == 1:
                solved.add(self.sudoku[(i+1,j+1)][0])
        for i,j in product(range(3*x-3, 3*x), range(3*y-3, 3*y)):
            if len(self.sudoku[(i+1,j+1)]) > 1:
                self.sudoku[(i+1,j+1)] = [k for k in self.sudoku[(i+1,j+1)] if k not in solved]    
    def reduce_3x3(self):
        for i,j in product(range(1,4), range(1,4)):
            self._reduce_3x3(i,j)
    
    def _reduce_row(self, n):
        solved = set()
        for i in range(1,10):
            if len(self.sudoku[(n,i)]) == 1:
                solved.add(self.sudoku[(n,i)][0])
        for i in range(1,10):
            if len(self.sudoku[(n,i)]) > 1:
                self.sudoku[(n,i)] = [k for k in self.sudoku[(n,i)] if k not in solved]
    def reduce_row(self):
        for i in range(1,10):
            self._reduce_row(i)
            
    def _reduce_col(self, n):
        solved = set()
        for i in range(1,10):
            if len(self.sudoku[(i,n)]) == 1:
                solved.add(self.sudoku[(i,n)][0])
        for i in range(1,10):
            if len(self.sudoku[(i,n)]) > 1:
                self.sudoku[(i,n)] = [k for k in self.sudoku[(i,n)] if k not in solved]
    def reduce_col(self):
        for i in range(1,10):
            self._reduce_col(i)
            
    def reduce(self):
        self.reduce_3x3()
        self.reduce_row()
        self.reduce_col()    
        
    
    def _col_locked(self, x,y):
        locked = set()
        for j in self._rest_of(y):
            locked.update(set(self.sudoku[(x,j)]))
        if not set(self.sudoku[(x,y)]).issubset(locked):
            self.sudoku[(x,y)] = [k for k in self.sudoku[(x,y)] if k not in locked]
            
    def _row_locked(self, x,y):
        locked = set()
        for i in self._rest_of(x):
            locked.update(set(self.sudoku[(i,y)]))
        if not set(self.sudoku[(x,y)]).issubset(locked):
            self.sudoku[(x,y)] = [k for k in self.sudoku[(x,y)] if k not in locked]
    
    def _3x3_locked(self,x,y):
        locked = set()
        for i,j in product(self._part_of(x), self._part_of(y)):
            if (i,j) != (x,y):
                locked.update(set(self.sudoku[(i,j)]))
        if not set(self.sudoku[(x,y)]).issubset(locked):
            self.sudoku[(x,y)] = [k for k in self.sudoku[(x,y)] if k not in locked]
    
    def _reduce_locked(self):
        for i,j in product(range(9), range(9)):
            self._col_locked(i+1,j+1)
            self._row_locked(i+1,j+1)
            self._3x3_locked(i+1,j+1)
    
    def _rest_of(self, x):
        if 1 <= x <= 3:
            rest = set(range(4,10))
        elif 4 <= x <= 6:
            rest = set(range(1,4)).union(set(range(7,10)))
        elif 7 <= x <= 9:
            rest = set(range(1,7))
        return rest
    
    def _part_of(self, x):
        if 1 <= x <= 3:
            part = set(range(1,4))
        elif 4 <= x <= 6:
            part = set(range(4,7))
        elif 7 <= x <= 9:
            part = set(range(7,10))
        return part
    

    
    def print_3x3(self, x, y):
        for i in range(3*x-3, 3*x):
            for j in range(3*y-3, 3*y):
                print(self.sudoku[(i+1,j+1)], end = " ")
            print()
           
    def missing(self):
        return sum(len(v) for v in self.sudoku.values()) - 81
    
    def solve(self):
        while self.missing() > 0:
            print('Values to reduce: ', self.missing())
            self.reduce()
            self._reduce_locked()
            self.reduce()
            
        return self.sudoku
    
    
    
#### Test ####

def fill_row(sudoku, n , indices, vals):
    for i, v in zip(indices, vals):
        sudoku.fill(n, i, v)
        
        
example = Sudoku()
fill_row(example, 1, [1,3,4,6,7], [3,6,5,8,4])
fill_row(example, 2, [1,2], [5,2])
fill_row(example, 3, [2,3,8,9], [8,7,3,1])
fill_row(example, 4, [3,5,8], [3,1,8])
fill_row(example, 5, [1,4,5,6,9], [9,8,6,3,5])
fill_row(example, 6, [2,5,7], [5,9,6])
fill_row(example, 7, [1,2,7,8], [1,3,2,5])
fill_row(example, 8, [8,9], [7,4])
fill_row(example, 9, [3,4,6,7], [5,2,6,3])
print(example.sudoku)

print(example.solve())