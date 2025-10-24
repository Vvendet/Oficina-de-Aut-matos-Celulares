import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# ---------------------------------
# Parâmetros
# ---------------------------------
GRID_SIZE = 50
PROB_INICIAL = 0.2  # probabilidade de célula viva na inicialização
INTERVALO = 100     # tempo entre frames (ms)

# ---------------------------------
# Criação da grade inicial
# ---------------------------------
def criar_grade():
    """Cria uma grade 2D com 0 (morto) e 1 (vivo)."""
    return np.random.choice([0, 1], size=(GRID_SIZE, GRID_SIZE), p=[1-PROB_INICIAL, PROB_INICIAL])

# ---------------------------------
# Funções de atualização
# ---------------------------------
def contar_vizinhos(grid, x, y):
    """Conta vizinhos vivos (vizinhança de Moore com bordas periódicas)."""
    total = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = (x + dx) % GRID_SIZE, (y + dy) % GRID_SIZE
            total += grid[nx, ny]
    return total

def proxima_geracao(grid):
    """Calcula a próxima geração segundo as regras de Conway."""
    nova = np.zeros_like(grid)
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            vivos = contar_vizinhos(grid, x, y)
            if grid[x, y] == 1:
                nova[x, y] = 1 if vivos in [2, 3] else 0
            else:
                nova[x, y] = 1 if vivos == 3 else 0
    return nova

# ---------------------------------
# Padrões famosos
# ---------------------------------
def inserir_glider(grid, x, y):
    coords = [(0,1), (1,2), (2,0), (2,1), (2,2)]
    for dx, dy in coords:
        grid[(x+dx)%GRID_SIZE, (y+dy)%GRID_SIZE] = 1

def inserir_blinker(grid, x, y):
    coords = [(0,0), (0,1), (0,2)]
    for dx, dy in coords:
        grid[(x+dx)%GRID_SIZE, (y+dy)%GRID_SIZE] = 1

def inserir_bloc(grid, x, y):
    coords = [(0,0), (0,1), (1,0), (1,1)]
    for dx, dy in coords:
        grid[(x+dx)%GRID_SIZE, (y+dy)%GRID_SIZE] = 1

# ---------------------------------
# Inicialização e inserção de padrões
# ---------------------------------
grid = criar_grade()

# Inserir padrões no centro (opcional)
cx, cy = GRID_SIZE // 2, GRID_SIZE // 2
inserir_glider(grid, cx-3, cy-3)
inserir_blinker(grid, cx+5, cy)
inserir_bloc(grid, cx-10, cy+8)

# ---------------------------------
# Visualização com Matplotlib
# ---------------------------------
fig, ax = plt.subplots()
img = ax.imshow(grid, interpolation='nearest', cmap='binary')
ax.set_title("Jogo da Vida de Conway")

def atualizar(frame_num):
    global grid
    grid = proxima_geracao(grid)
    img.set_data(grid)
    return img,

ani = animation.FuncAnimation(fig, atualizar, interval=INTERVALO, save_count=200)
plt.show()
