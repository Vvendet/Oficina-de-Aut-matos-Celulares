import tkinter as tk
import random

# ------------------- PARÂMETROS GERAIS -------------------
ROWS = 50
COLS = 50
CELL_SIZE = 10
DELAY = 100  # milissegundos

running = False  # estado da simulação
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# ------------------- FUNÇÕES PRINCIPAIS -------------------

def draw_grid():
    """Desenha toda a grade no canvas."""
    canvas.delete("all")
    for i in range(ROWS):
        for j in range(COLS):
            x1 = j * CELL_SIZE
            y1 = i * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            color = "black" if grid[i][j] == 1 else "white"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

def count_neighbors(i, j):
    """Conta os vizinhos vivos (vizinhança de Moore)."""
    count = 0
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            if di == 0 and dj == 0:
                continue
            ni, nj = i + di, j + dj
            if 0 <= ni < ROWS and 0 <= nj < COLS:
                count += grid[ni][nj]
    return count

def update_grid():
    """Aplica as regras do Jogo da Vida e atualiza a grade."""
    global grid
    new_grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    for i in range(ROWS):
        for j in range(COLS):
            neighbors = count_neighbors(i, j)
            if grid[i][j] == 1:
                new_grid[i][j] = 1 if neighbors in (2, 3) else 0
            else:
                new_grid[i][j] = 1 if neighbors == 3 else 0
    grid = new_grid
    draw_grid()

def run_simulation():
    """Executa continuamente a simulação."""
    if running:
        update_grid()
        root.after(DELAY, run_simulation)

# ------------------- CONTROLE E INTERAÇÃO -------------------

def start():
    """Inicia a simulação."""
    global running
    running = True
    run_simulation()

def stop():
    """Pausa a simulação."""
    global running
    running = False

def clear():
    """Limpa a grade."""
    global grid
    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    draw_grid()

def randomize():
    """Preenche a grade aleatoriamente."""
    global grid
    grid = [[random.randint(0, 1) for _ in range(COLS)] for _ in range(ROWS)]
    draw_grid()

def toggle_cell(event):
    """Ativa/desativa uma célula ao clicar."""
    j = event.x // CELL_SIZE
    i = event.y // CELL_SIZE
    if 0 <= i < ROWS and 0 <= j < COLS:
        grid[i][j] = 1 - grid[i][j]
        draw_grid()

# ------------------- PADRÕES FAMOSOS -------------------

def insert_pattern(pattern_name):
    """Insere um padrão famoso centralizado."""
    global grid
    clear()
    center_i, center_j = ROWS // 2, COLS // 2

    if pattern_name == "Glider":
        pattern = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
    elif pattern_name == "Oscilador":
        pattern = [(0, 1), (1, 1), (2, 1)]
    elif pattern_name == "Bloco":
        pattern = [(0, 0), (0, 1), (1, 0), (1, 1)]
    else:
        pattern = []

    for di, dj in pattern:
        i = center_i + di
        j = center_j + dj
        if 0 <= i < ROWS and 0 <= j < COLS:
            grid[i][j] = 1

    draw_grid()

# ------------------- INTERFACE GRÁFICA -------------------

root = tk.Tk()
root.title("Jogo da Vida de Conway")

canvas = tk.Canvas(root, width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE, bg="white")
canvas.pack()
canvas.bind("<Button-1>", toggle_cell)

frame = tk.Frame(root)
frame.pack(pady=5)

start_button = tk.Button(frame, text="Iniciar", command=start)
start_button.pack(side=tk.LEFT, padx=5)

stop_button = tk.Button(frame, text="Pausar", command=stop)
stop_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(frame, text="Limpar", command=clear)
clear_button.pack(side=tk.LEFT, padx=5)

random_button = tk.Button(frame, text="Aleatório", command=randomize)
random_button.pack(side=tk.LEFT, padx=5)

pattern_var = tk.StringVar(value="Escolher padrão")
pattern_menu = tk.OptionMenu(frame, pattern_var, "Glider", "Oscilador", "Bloco", command=insert_pattern)
pattern_menu.pack(side=tk.LEFT, padx=10)

draw_grid()
root.mainloop()
