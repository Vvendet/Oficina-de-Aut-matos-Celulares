import tkinter as tk
import random

# -----------------------------
# Parâmetros principais
# -----------------------------
GRID_SIZE = 50     # número de células por linha e coluna
CELL_SIZE = 10     # tamanho de cada célula em pixels
UPDATE_DELAY = 100 # tempo entre atualizações (ms)

# -----------------------------
# Criação da grade
# -----------------------------
def criar_grade():
    """Cria uma grade 2D com células mortas (0)."""
    return [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# -----------------------------
# Atualização da grade
# -----------------------------
def contar_vizinhos(grid, x, y):
    """Conta vizinhos vivos (vizinhança de Moore)."""
    vizinhos = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = (x + dx) % GRID_SIZE, (y + dy) % GRID_SIZE
            vizinhos += grid[nx][ny]
    return vizinhos

def proxima_geracao(grid):
    """Calcula a próxima geração segundo as regras de Conway."""
    nova = criar_grade()
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            vivos = contar_vizinhos(grid, x, y)
            if grid[x][y] == 1:
                nova[x][y] = 1 if vivos in [2, 3] else 0
            else:
                nova[x][y] = 1 if vivos == 3 else 0
    return nova

# -----------------------------
# Desenho na tela
# -----------------------------
def desenhar(canvas, grid):
    """Desenha a grade atual no canvas."""
    canvas.delete("all")
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if grid[x][y] == 1:
                canvas.create_rectangle(
                    y * CELL_SIZE, x * CELL_SIZE,
                    (y + 1) * CELL_SIZE, (x + 1) * CELL_SIZE,
                    fill="black", outline="gray"
                )

# -----------------------------
# Padrões famosos
# -----------------------------
def inserir_glider(grid, x, y):
    """Insere um glider começando na posição (x, y)."""
    coords = [(0,1), (1,2), (2,0), (2,1), (2,2)]
    for dx, dy in coords:
        grid[(x+dx)%GRID_SIZE][(y+dy)%GRID_SIZE] = 1

def inserir_blinker(grid, x, y):
    """Insere um oscilador blinker."""
    coords = [(0,0), (0,1), (0,2)]
    for dx, dy in coords:
        grid[(x+dx)%GRID_SIZE][(y+dy)%GRID_SIZE] = 1

def inserir_bloc(grid, x, y):
    """Insere um bloco estável."""
    coords = [(0,0), (0,1), (1,0), (1,1)]
    for dx, dy in coords:
        grid[(x+dx)%GRID_SIZE][(y+dy)%GRID_SIZE] = 1

# -----------------------------
# Controle do jogo
# -----------------------------
def atualizar():
    global grid, rodando
    if rodando:
        grid = proxima_geracao(grid)
        desenhar(canvas, grid)
        root.after(UPDATE_DELAY, atualizar)

def alternar_celula(event):
    """Permite ativar/desativar células com o clique do mouse."""
    x, y = event.y // CELL_SIZE, event.x // CELL_SIZE
    grid[x][y] = 1 - grid[x][y]
    desenhar(canvas, grid)

def iniciar_parar():
    """Inicia ou pausa o jogo."""
    global rodando
    rodando = not rodando
    if rodando:
        atualizar()

def limpar():
    """Limpa a grade."""
    global grid
    grid = criar_grade()
    desenhar(canvas, grid)

def inserir_padrao(padrao):
    """Insere um padrão pré-definido no centro."""
    global grid
    x, y = GRID_SIZE // 2, GRID_SIZE // 2
    if padrao == "glider":
        inserir_glider(grid, x, y)
    elif padrao == "blinker":
        inserir_blinker(grid, x, y)
    elif padrao == "bloco":
        inserir_bloc(grid, x, y)
    desenhar(canvas, grid)

# -----------------------------
# Interface Tkinter
# -----------------------------
root = tk.Tk()
root.title("Jogo da Vida de Conway")

canvas = tk.Canvas(root, width=GRID_SIZE*CELL_SIZE, height=GRID_SIZE*CELL_SIZE, bg="white")
canvas.pack()

frame = tk.Frame(root)
frame.pack()

btn_iniciar = tk.Button(frame, text="▶ Iniciar / Pausar", command=iniciar_parar)
btn_iniciar.pack(side=tk.LEFT, padx=5)

btn_limpar = tk.Button(frame, text="🧹 Limpar", command=limpar)
btn_limpar.pack(side=tk.LEFT, padx=5)

btn_glider = tk.Button(frame, text="🪶 Glider", command=lambda: inserir_padrao("glider"))
btn_glider.pack(side=tk.LEFT, padx=5)

btn_blinker = tk.Button(frame, text="🔁 Blinker", command=lambda: inserir_padrao("blinker"))
btn_blinker.pack(side=tk.LEFT, padx=5)

btn_bloc = tk.Button(frame, text="⬛ Bloco", command=lambda: inserir_padrao("bloco"))
btn_bloc.pack(side=tk.LEFT, padx=5)

canvas.bind("<Button-1>", alternar_celula)

# -----------------------------
# Inicialização
# -----------------------------
grid = criar_grade()
rodando = False
desenhar(canvas, grid)

root.mainloop()
