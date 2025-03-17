import random
import time
import copy

class Sudoku:
    def __init__(self):
        # Initialize empty 9x9 grid
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solution = None
    
    def print_board(self):
        """Print the Sudoku board in a readable format"""
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - - - -")
            
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    print("| ", end="")
                    
                # Display underscore for empty cells (0)
                display_char = "_" if self.board[i][j] == 0 else self.board[i][j]
                
                if j == 8:
                    print(display_char)
                else:
                    print(str(display_char) + " ", end="")
    
    def find_empty(self):
        """Find an empty cell in the board"""
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j)  # row, column
        return None
    
    def valid(self, num, pos):
        """Check if the number can be placed at the given position"""
        # Check row
        for j in range(9):
            if self.board[pos[0]][j] == num and pos[1] != j:
                return False
        
        # Check column
        for i in range(9):
            if self.board[i][pos[1]] == num and pos[0] != i:
                return False
        
        # Check 3x3 box
        box_x = pos[1] // 3
        box_y = pos[0] // 3
        
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if self.board[i][j] == num and (i, j) != pos:
                    return False
        
        return True
    
    def solve(self):
        """Solve the Sudoku using backtracking"""
        find = self.find_empty()
        if not find:
            return True
        else:
            row, col = find
        
        for num in range(1, 10):
            if self.valid(num, (row, col)):
                self.board[row][col] = num
                
                if self.solve():
                    return True
                
                # Backtrack if the solution doesn't work
                self.board[row][col] = 0
        
        return False
    
    def generate(self, difficulty='medium'):
        """Generate a new Sudoku puzzle with specified difficulty
        
        Difficulty levels:
        - easy: 35-40 empty cells
        - medium: 41-49 empty cells
        - hard: 50-59 empty cells
        - expert: 60+ empty cells
        """
        # Reset the board
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        
        # Fill the diagonal 3x3 boxes (these can be filled independently)
        for i in range(0, 9, 3):
            self._fill_box(i, i)
        
        # Fill the rest using the solver
        self.solve()
        
        # Store the solution
        self.solution = copy.deepcopy(self.board)
        
        # Remove numbers based on difficulty
        cells_to_remove = {
            'easy': random.randint(35, 40),
            'medium': random.randint(41, 49),
            'hard': random.randint(50, 59),
            'expert': random.randint(60, 65)
        }.get(difficulty.lower(), 45) 
        
        self._remove_numbers(cells_to_remove)
        
        return self.board
    
    def _fill_box(self, row, col):
        """Fill a 3x3 box with random numbers"""
        nums = list(range(1, 10))
        random.shuffle(nums)
        
        for i in range(3):
            for j in range(3):
                self.board[row + i][col + j] = nums.pop()
    
    def _remove_numbers(self, count):
        """Remove specified number of cells while ensuring unique solution"""
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        
        for i, j in cells:
            if count <= 0:
                break
                
            backup = self.board[i][j]
            self.board[i][j] = 0
            
            if self._has_unique_solution():
                count -= 1
            else:
                self.board[i][j] = backup
    
    def _has_unique_solution(self):
        """Check if the puzzle has a unique solution
        This is a simplified check, it does not guarantee uniqueness but works well enough
        """
        board_copy = copy.deepcopy(self.board)
        
        test_sudoku = Sudoku()
        test_sudoku.board = board_copy
        if not test_sudoku.solve():
            return False
            
        return True
    
    def check_solution(self, user_solution):
        """Check if the user's solution matches the correct solution"""
        if self.solution is None:
            raise ValueError("No solution available. Generate a puzzle first.")
            
        return user_solution == self.solution

    def get_difficulty_estimate(self):
        """Estimate the difficulty of the current puzzle"""
        empty_cells = sum(row.count(0) for row in self.board)
        
        if empty_cells <= 40:
            return "Easy"
        elif empty_cells <= 49:
            return "Medium"
        elif empty_cells <= 59:
            return "Hard"
        else:
            return "Expert"


def main():
    sudoku = Sudoku()
    
    print("Generating a new Sudoku puzzle...")
    difficulty = input("Choose difficulty (easy/medium/hard/expert): ").strip() or "medium"
    
    start_time = time.time()
    sudoku.generate(difficulty)
    generation_time = time.time() - start_time
    
    print(f"\nGenerated {sudoku.get_difficulty_estimate()} puzzle in {generation_time:.2f} seconds:")
    sudoku.print_board()
    
    print("\nOptions:")
    print("1. Solve the puzzle automatically")
    print("2. Exit")
    
    choice = input("\nEnter your choice (1-2): ").strip()
    
    if choice == "1":
        print("\nSolving...")
        solution = Sudoku()
        solution.board = copy.deepcopy(sudoku.board)
        
        start_time = time.time()
        if solution.solve():
            solving_time = time.time() - start_time
            print(f"\nSolved in {solving_time:.2f} seconds:")
            solution.print_board()
        else:
            print("No solution exists!")
    
    print("\nThanks for playing!")

if __name__ == "__main__":
    main()