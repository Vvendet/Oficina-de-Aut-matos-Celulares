import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# -------------------------------
# Parâmetros da simulação
# -------------------------------
N = 80               # tamanho da grade
D = 0.2              # coeficiente de difusão (0 < D < 0.25 para estabilidade)
INTERVALO = 50       # intervalo entre frames (ms)

# -------------------------------
# Inicialização da grade
# -------------------------------
def inicializar_grade():
    """Cria uma matriz de densidades com uma 'gota' central de fluido."""
    grid = np.zeros((N, N))
    cx, cy = N // 2, N // 2
    grid[cx-3:cx+3, cy-3:cy+3] = 2.0   # gota inicial no centro
    return grid

# -------------------------------
# Atualização das células
# -------------------------------
def atualizar(grid):
    """Atualiza o estado do autômato (difusão local)."""
    new_grid = grid.copy()
    for i in range(1, N-1):
        for j in range(1, N-1):
            # regra de difusão (média dos vizinhos)
            vizinhos = (
                grid[i-1, j] + grid[i+1, j] +
                grid[i, j-1] + grid[i, j+1]
            )
            new_grid[i, j] = grid[i, j] + D * (vizinhos - 4 * grid[i, j])
    return new_grid

# -------------------------------
# Visualização
# -------------------------------
grid = inicializar_grade()
fig, ax = plt.subplots()
img = ax.imshow(grid, cmap='viridis', interpolation='nearest', vmin=0, vmax=1)
ax.set_title("Simulação de Fluido via Autômato Celular")

def animar(frame):
    global grid
    grid = atualizar(grid)
    img.set_data(grid)
    return [img]

ani = animation.FuncAnimation(fig, animar, interval=INTERVALO, blit=True)
plt.show()
