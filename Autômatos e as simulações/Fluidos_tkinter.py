import tkinter as tk
import random
import time

# -------------------------------
# Parâmetros da simulação
# -------------------------------
N = 50              # tamanho da grade
CELL_SIZE = 5       # tamanho de cada célula em pixels
D = 0.3            # coeficiente de difusão (0 < D < 0.3 para estabilidade)
INTERVALO = 25      # intervalo entre frames em ms

# -------------------------------
# Inicialização da grade
# -------------------------------
def inicializar_grade():
    """Cria uma matriz de densidades com uma 'gota' central de fluido."""
    grid = [[0.0 for _ in range(N)] for _ in range(N)]
    cx, cy = N // 2, N // 2
    for i in range(cx - 3, cx + 3):
        for j in range(cy - 3, cy + 3):
            grid[i][j] = 2.0  # gota inicial
    return grid

# -------------------------------
# Atualização da grade (vizinhança de Moore)
# -------------------------------
def atualizar(grid):
    new_grid = [[grid[i][j] for j in range(N)] for i in range(N)]
    for i in range(1, N - 1):
        for j in range(1, N - 1):
            vizinhos = (
                grid[i - 1][j] + grid[i + 1][j] +
                grid[i][j - 1] + grid[i][j + 1] +
                grid[i - 1][j - 1] + grid[i - 1][j + 1] +
                grid[i + 1][j - 1] + grid[i + 1][j + 1]
            )
            new_grid[i][j] = grid[i][j] + D * (vizinhos - 8 * grid[i][j]) / 8
    return new_grid

# -------------------------------
# Cores e visualização
# -------------------------------
def valor_para_cor(valor):
    """Converte um valor de densidade em uma cor azulada."""
    valor = max(0.0, min(1.0, valor))  # limitar entre 0 e 1
    intensidade = int(255 * valor)
    return f"#0000{intensidade:02x}"  # tons de azul

def desenhar_grid():
    """Atualiza a visualização da grade no canvas."""
    canvas.delete("all")
    for i in range(N):
        for j in range(N):
            cor = valor_para_cor(min(grid[i][j], 1.0))
            x1, y1 = j * CELL_SIZE, i * CELL_SIZE
            x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
            canvas.create_rectangle(x1, y1, x2, y2, fill=cor, outline="")

# -------------------------------
# Loop de animação
# -------------------------------
rodando = False

def iniciar():
    global rodando
    if not rodando:
        rodando = True
        atualizar_animacao()

def pausar():
    global rodando
    rodando = False

def atualizar_animacao():
    global grid
    if rodando:
        grid = atualizar(grid)
        desenhar_grid()
        root.after(INTERVALO, atualizar_animacao)

def limpar():
    global grid
    pausar()
    grid = [[0.0 for _ in range(N)] for _ in range(N)]
    desenhar_grid()

# -------------------------------
# Interface Tkinter
# -------------------------------
root = tk.Tk()
root.title("Simulação de Fluido via Autômato Celular (Tkinter)")

canvas = tk.Canvas(root, width=N * CELL_SIZE, height=N * CELL_SIZE, bg="white")
canvas.pack(pady=5)

frame = tk.Frame(root)
frame.pack()

start_button = tk.Button(frame, text="Iniciar", command=iniciar)
start_button.pack(side=tk.LEFT, padx=5)

pause_button = tk.Button(frame, text="Pausar", command=pausar)
pause_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(frame, text="Limpar", command=limpar)
clear_button.pack(side=tk.LEFT, padx=5)

# Inicialização da simulação
grid = inicializar_grade()
desenhar_grid()

root.mainloop()
