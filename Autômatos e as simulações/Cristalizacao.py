import pygame
import numpy as np
import random
from sys import exit

# ----------------------------------
# Parâmetros
# ----------------------------------
SCREEN_SIZE = 600
CELL_SIZE = 3
GRID_SIZE = SCREEN_SIZE // CELL_SIZE
FPS = 60

COR_FUNDO = (0, 0, 20)
COR_CRISTAL = (120, 200, 255)

# ----------------------------------
# Inicialização
# ----------------------------------
pygame.init()
tela = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Crescimento Cristalino — Autômato Celular")
clock = pygame.time.Clock()

grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.uint8)
centro = GRID_SIZE // 2
grid[centro, centro] = 1  # núcleo inicial

# ----------------------------------
# Funções
# ----------------------------------
def atualizar():
    """Regra de crescimento cristalino."""
    global grid
    nova = np.copy(grid)
    for i in range(1, GRID_SIZE - 1):
        for j in range(1, GRID_SIZE - 1):
            if grid[i, j] == 0:
                vizinhos = np.sum(grid[i - 1:i + 2, j - 1:j + 2]) - grid[i, j]
                if vizinhos > 0 and random.random() < 0.15:  # probabilidade de cristalizar
                    nova[i, j] = 1
    grid = nova

def desenhar():
    """Renderiza o cristal."""
    tela.fill(COR_FUNDO)
    y, x = np.where(grid == 1)
    for px, py in zip(x, y):
        pygame.draw.rect(tela, COR_CRISTAL, (px * CELL_SIZE, py * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.flip()

# ----------------------------------
# Loop principal
# ----------------------------------
while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    atualizar()
    desenhar()
