import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# -------------------------------
# Parâmetros da simulação
# -------------------------------
N = 80               # tamanho da grade
D = 0.3              # coeficiente de difusão (0 < D < 0.3 para estabilidade)
INTERVALO = 50       # intervalo entre frames (ms)

# -------------------------------
# Inicialização da grade
# -------------------------------
def inicializar_grade():
    """Cria uma matriz de densidades com uma 'gota' central de fluido."""
    grid = [[0.0 for _ in range(N)] for _ in range(N)]
    cx, cy = N // 2, N // 2
    for i in range(cx - 3, cx + 3):
        for j in range(cy - 3, cy + 3):
            grid[i][j] = 2.0
    return grid

# -------------------------------
# Atualização das células
# -------------------------------
def atualizar(grid):
    """Atualiza o estado da grade com base na difusão local (vizinhança de Moore)."""
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
# Visualização
# -------------------------------
grid = inicializar_grade()
fig, ax = plt.subplots()
img = ax.imshow(grid, cmap='viridis', interpolation='nearest', vmin=0, vmax=1)
ax.set_title("Simulação de Fluido via Autômato Celular (sem NumPy)")

def animar(frame):
    global grid
    grid = atualizar(grid)
    img.set_data(grid)
    return [img]

ani = animation.FuncAnimation(fig, animar, interval=INTERVALO, blit=True)
plt.show()
