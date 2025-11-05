import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def generate_rule_dict(rule_number):
    """Converte número da regra em um dicionário de transições."""
    binary_rule = np.array([int(x) for x in np.binary_repr(rule_number, width=8)])
    patterns = [tuple(map(int, np.binary_repr(i, width=3))) for i in range(8)]
    return {patterns[i]: binary_rule[7 - i] for i in range(8)}

def evolve(rule_dict, width=201, generations=100):
    """Gera a evolução do autômato celular 1D."""
    grid = np.zeros((generations, width), dtype=int)
    grid[0, width // 2] = 1
    for t in range(1, generations):
        for i in range(1, width - 1):
            neighborhood = (grid[t - 1, i - 1], grid[t - 1, i], grid[t - 1, i + 1])
            grid[t, i] = rule_dict[neighborhood]
    return grid

def plot_rule(rule_number):
    """Gera e exibe o autômato para a regra escolhida."""
    rule_dict = generate_rule_dict(rule_number)
    grid = evolve(rule_dict)
    ax.clear()
    ax.imshow(grid, cmap='binary', interpolation='nearest', origin='upper')
    ax.set_title(f"Regra {rule_number}")
    ax.axis('off')
    fig.canvas.draw_idle()

# --- Interface interativa ---
fig, ax = plt.subplots(figsize=(8, 8))
plt.subplots_adjust(bottom=0.25)

# Padrão inicial
initial_rule = 90
plot_rule(initial_rule)

# Slider
ax_slider = plt.axes([0.2, 0.1, 0.6, 0.03])
rule_slider = Slider(ax_slider, "Regra", 0, 255, valinit=initial_rule, valstep=1)

def update(val):
    rule = int(rule_slider.val)
    plot_rule(rule)

rule_slider.on_changed(update)
plt.show()
