import tkinter as tk
import random
import time

ROWS = 15          
COLS = 20          
CELL_SIZE = 30     
OFFSET = 40        

northWall = [[1 for _ in range(COLS + 1)] for _ in range(ROWS + 1)]
eastWall = [[1 for _ in range(COLS + 1)] for _ in range(ROWS + 1)]
visited = [[0 for _ in range(COLS + 1)] for _ in range(ROWS + 1)]

root = tk.Tk()
root.title("Dynamic Maze Generator and Solver")

canvas_width = COLS * CELL_SIZE + (OFFSET * 2)
canvas_height = ROWS * CELL_SIZE + (OFFSET * 2)
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

def draw_maze():
    """Clears the canvas and redraws all walls currently set to 1."""
    canvas.delete("all")
    
    for r in range(1, ROWS + 1):
        for c in range(1, COLS + 1):
            x1 = OFFSET + (c - 1) * CELL_SIZE
            y1 = OFFSET + (ROWS - r) * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            
            
            if northWall[r][c] == 1:
                canvas.create_line(x1, y1, x2, y1, width=2, fill="black")
                
            
            if eastWall[r][c] == 1:
                canvas.create_line(x2, y1, x2, y2, width=2, fill="black")
                
            
            if c == 1 and eastWall[r][0] == 1:
                canvas.create_line(x1, y1, x1, y2, width=2, fill="black")
                
            
            if northWall[r-1][c] == 1:
                canvas.create_line(x1, y2, x2, y2, width=2, fill="black")

    root.update()

def generate_maze(start_r, start_c):
    """Generates a proper maze with loop injections using a stack."""
    stack = []
    current_cell = (start_r, start_c)
    visited[start_r][start_c] = 1
    
    
    entrance_row = ROWS // 2
    eastWall[entrance_row][0] = 0 
    
    
    eastWall[1][COLS] = 0 

    while True:
        r, c = current_cell
        neighbors = []
        
        if r < ROWS and not visited[r + 1][c]: neighbors.append(('N', r + 1, c))
        if c < COLS and not visited[r][c + 1]: neighbors.append(('E', r, c + 1))
        if r > 1 and not visited[r - 1][c]:    neighbors.append(('S', r - 1, c))
        if c > 1 and not visited[r][c - 1]:    neighbors.append(('W', r, c - 1))
        
        if neighbors:
            direction, nr, nc = random.choice(neighbors)
            
            
            if direction == 'N': northWall[r][c] = 0
            elif direction == 'E': eastWall[r][c] = 0
            elif direction == 'S': northWall[r - 1][c] = 0
            elif direction == 'W': eastWall[nr][nc] = 0
            
            
            if random.randint(1, 20) == 1:
                all_neighbors = []
                if r < ROWS: all_neighbors.append(('N', r, c))
                if c < COLS: all_neighbors.append(('E', r, c))
                if all_neighbors:
                    bonus_dir, br, bc = random.choice(all_neighbors)
                    if bonus_dir == 'N': northWall[br][bc] = 0
                    else: eastWall[br][bc] = 0
            
            stack.append(current_cell)
            visited[nr][nc] = 1
            current_cell = (nr, nc)
            
            draw_maze()
            time.sleep(0.01)
            
        elif stack:
            current_cell = stack.pop()
        else:
            break

    
    root.after(500, solve_maze)

def solve_maze():
    """Finds the solution path using a red locator and blue dead-end dots."""
    start_row = ROWS // 2
    target_cell = (1, COLS)
    
    stack = [(start_row, 1)]
    solver_visited = set()
    solver_visited.add((start_row, 1))
    
    
    active_dots = {}
    
    while stack:
        r, c = stack[-1] 
        
        
        x_mid = OFFSET + (c - 1) * CELL_SIZE + (CELL_SIZE // 2)
        y_mid = OFFSET + (ROWS - r) * CELL_SIZE + (CELL_SIZE // 2)
        
        
        if (r, c) not in active_dots:
            dot = canvas.create_oval(x_mid-6, y_mid-6, x_mid+6, y_mid+6, fill="red")
            active_dots[(r, c)] = dot
        
        canvas.tag_raise("all")
        root.update()
        time.sleep(0.06) 
        
        if (r, c) == target_cell:
            break
            
        accessible_options = []
        
        
        if r < ROWS and northWall[r][c] == 0 and (r + 1, c) not in solver_visited:
            accessible_options.append((r + 1, c))
        if c < COLS and eastWall[r][c] == 0 and (r, c + 1) not in solver_visited:
            accessible_options.append((r, c + 1))
        if r > 1 and northWall[r - 1][c] == 0 and (r - 1, c) not in solver_visited:
            accessible_options.append((r - 1, c))
        if c > 1 and eastWall[r][c - 1] == 0 and (r, c - 1) not in solver_visited:
            accessible_options.append((r, c - 1))
            
        if accessible_options:
            next_cell = random.choice(accessible_options)
            solver_visited.add(next_cell)
            stack.append(next_cell)
        else:
            
            canvas.create_oval(x_mid-5, y_mid-5, x_mid+5, y_mid+5, fill="blue")
            if (r, c) in active_dots:
                canvas.delete(active_dots[(r, c)])
                del active_dots[(r, c)]
            stack.pop()
            root.update()

draw_maze()
root.after(1000, lambda: generate_maze(ROWS, 1)) 
root.mainloop()