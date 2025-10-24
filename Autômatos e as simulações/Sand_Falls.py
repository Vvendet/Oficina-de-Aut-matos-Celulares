import pygame
import numpy as np
from sys import exit

# ----------------------------------
# Parâmetros
# ----------------------------------
SCREEN_SIZE = 600
CELL_SIZE = 5
GRID_SIZE = SCREEN_SIZE // CELL_SIZE
FPS = 60

COR_AREIA = (255, 230, 80)
COR_FUNDO = (0, 0, 0)
COR_PAREDE = (100, 100, 100)

# ----------------------------------
# Inicialização
# ----------------------------------
pygame.init()
tela = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Simulação de Areia — Autômato Celular")
clock = pygame.time.Clock()

# 0 = vazio | 1 = areia | 2 = parede
grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.uint8)

# ----------------------------------
# Funções auxiliares
# ----------------------------------
def desenhar():
    """Renderiza a grade na tela."""
    tela.fill(COR_FUNDO)
    areia_y, areia_x = np.where(grid == 1)
    parede_y, parede_x = np.where(grid == 2)
    for x, y in zip(areia_x, areia_y):
        pygame.draw.rect(tela, COR_AREIA, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    for x, y in zip(parede_x, parede_y):
        pygame.draw.rect(tela, COR_PAREDE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.flip()

def atualizar():
    """Aplica as regras do autômato para atualizar a posição da areia."""
    global grid
    nova = np.copy(grid)

    # Percorre de baixo para cima (para evitar sobreposição de grãos)
    for j in range(GRID_SIZE - 2, -1, -1):
        for i in range(1, GRID_SIZE - 1):
            if grid[j, i] == 1:  # célula com areia
                # Queda vertical
                if grid[j + 1, i] == 0:
                    nova[j, i] = 0
                    nova[j + 1, i] = 1
                # Diagonal esquerda
                elif grid[j + 1, i - 1] == 0:
                    nova[j, i] = 0
                    nova[j + 1, i - 1] = 1
                # Diagonal direita
                elif grid[j + 1, i + 1] == 0:
                    nova[j, i] = 0
                    nova[j + 1, i + 1] = 1
    grid = nova

def adicionar_areia(pos, tipo=1):
    """Adiciona areia ou parede com base no clique."""
    x, y = pos[0] // CELL_SIZE, pos[1] // CELL_SIZE
    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
        grid[y, x] = tipo

# ----------------------------------
# Loop principal
# ----------------------------------
modo_parede = False
arrastando = False

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                grid.fill(0)
            elif event.key == pygame.K_p:
                modo_parede = not modo_parede  # alternar entre areia e parede
        elif event.type == pygame.MOUSEBUTTONDOWN:
            arrastando = True
            adicionar_areia(event.pos, tipo=2 if modo_parede else 1)
        elif event.type == pygame.MOUSEBUTTONUP:
            arrastando = False
        elif event.type == pygame.MOUSEMOTION and arrastando:
            adicionar_areia(event.pos, tipo=2 if modo_parede else 1)

    atualizar()
    desenhar()
