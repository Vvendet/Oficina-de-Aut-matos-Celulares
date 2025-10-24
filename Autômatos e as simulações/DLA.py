import tkinter as tk
import random
import math
import time

# Parâmetros
GRID_SIZE = 201   # tamanho da grade (ímpar, para ter centro)
NUM_PARTICLES = 1500
DELAY = 1  # atraso em ms entre atualizações para visualização

# Inicializa a grade
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
center = GRID_SIZE // 2
grid[center][center] = 1  # semente inicial no centro

# Janela Tkinter
CELL_SIZE = 3
root = tk.Tk()
root.title("Difusão Limitada por Agregação (DLA)")
canvas = tk.Canvas(root, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE, bg="black")
canvas.pack()

# Desenha um ponto
def draw_cell(x, y, color="white"):
    canvas.create_rectangle(
        x * CELL_SIZE, y * CELL_SIZE,
        (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
        fill=color, outline=""
    )

draw_cell(center, center, "cyan")

# Função auxiliar: verifica se um ponto toca o aglomerado
def touches_cluster(x, y):
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if 0 <= x+dx < GRID_SIZE and 0 <= y+dy < GRID_SIZE:
                if grid[y+dy][x+dx] == 1:
                    return True
    return False

# Criação de partículas
def random_edge_position():
    """Sorteia posição inicial nas bordas"""
    side = random.choice(["top", "bottom", "left", "right"])
    if side == "top":
        return random.randint(0, GRID_SIZE-1), 0
    elif side == "bottom":
        return random.randint(0, GRID_SIZE-1), GRID_SIZE-1
    elif side == "left":
        return 0, random.randint(0, GRID_SIZE-1)
    else:
        return GRID_SIZE-1, random.randint(0, GRID_SIZE-1)

# Loop principal
def simulate():
    for _ in range(NUM_PARTICLES):
        x, y = random_edge_position()

        # Caminho aleatório
        for _ in range(5000):  # limite de passos
            # Movimento aleatório
            dx, dy = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
            x = (x + dx) % GRID_SIZE
            y = (y + dy) % GRID_SIZE

            if touches_cluster(x, y):
                grid[y][x] = 1
                color = f"#{random.randint(80,255):02x}{random.randint(80,255):02x}{255:02x}"
                draw_cell(x, y, color)
                canvas.update()
                root.after(DELAY)
                break

            # Sai se estiver muito longe do centro
            if math.dist((x,y), (center,center)) > GRID_SIZE/2:
                break

    print("Simulação concluída.")
    canvas.update()

root.after(500, simulate)
root.mainloop()
