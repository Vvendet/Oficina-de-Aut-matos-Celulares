import tkinter as tk
import random

ROWS = 10
COLS = 10
CELL_SIZE = 10

grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

DELAY = 100

running = False

#########

def draw_grid():
    canvas.delete("all")
    for i in range(ROWS):
        for j in range(COLS):
            x1 = j*CELL_SIZE
            y1 = i*CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            color = "black" if grid[i][j] == 1 else "white"
            canvas.create_rectangle(x1,y1,x2,y2, fill=color, outline="gray")

def vizinhanca(i,j):
    count = 0 
    for di in (-1,0,1):
        for dj in (-1,0,1):
            if di == 0 and dj == 0:
                continue
            ni,nj = i+di,j+dj
            if (0<=ni < ROWS) and 0<=nj < COLS:
                count += grid[ni][nj]
    return count

def update_grid():
    global grid
    new_grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    for i in range(ROWS):
        for j in range(COLS):
            vizinhos_vivos = vizinhanca(i,j)
            if grid[i][j]==1:
                new_grid[i][j] = 1 if vizinhos_vivos in (2,3) else 0
            else:
                new_grid[i][j]= 1 if vizinhos_vivos == 3 else 0

    grid = new_grid
    draw_grid()

def toggle_cell(event):
    j = event.x // CELL_SIZE
    i = event.y // CELL_SIZE
    if 0<= i < ROWS and 0 <= j < COLS:
        grid[i][j] = 1 - grid[i][j]
        draw_grid()


def run_simulation():
    global running
    if running:
        update_grid()
        root.after(DELAY,run_simulation)

def start():
    global running
    running = True
    run_simulation()

def stop():
    global running
    running = False

def randomizar():
    global grid

    grid = [[random.randint(0,1) for _ in range(ROWS)] for _ in range(COLS)]
    draw_grid()

def clear():
    global grid

    grid = [[0 for _ in range(ROWS)] for _ in range(COLS)]
    draw_grid()
#########

root = tk.Tk()
root.title("Jogo da Vida")

canvas = tk.Canvas(root, width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE, bg="white")
canvas.pack()
canvas.bind("<Button-1>",toggle_cell)

frame = tk.Frame(root)
frame.pack(pady=5)

start_button = tk.Button(frame, text="Iniciar", command=start)
start_button.pack(side=tk.LEFT, padx=5)

stop_button = tk.Button(frame, text="Parar", command=stop)
stop_button.pack(side=tk.LEFT, padx=5)

random_button = tk.Button(frame, text="Aleatório", command=randomizar)
random_button.pack(side=tk.LEFT, padx=10)

clear_button = tk.Button(frame, text="Limpar", command=clear)
clear_button.pack(side=tk.LEFT, padx=10)

root.mainloop()