import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors # <-- 1. Importar módulo de colores
# =========================
# Leer archivo
# =========================

# =========================
# Matriz de densidad
# Filas  -> llaves (0-255)
# Columnas -> rondas (1-50)
# =========================

cicles_per_round = np.zeros((51), dtype=int)


for i in range(32):
    filename = f"fixed-point-thread-{i}.txt"
    print(f"Procesando {filename}...")
    with open(filename, "r") as f:
        lines = f.readlines()

    # =========================
    # Parsear líneas
    # =========================

    pattern = r"Rounds:\s*(\d+)\s*\|\s*Key:\s*([0-9a-fA-F]+)"
    j=0

    for line in lines:
        j += 1
        line = line.strip()
        match = re.search(pattern, line)

        if match:

            rounds = int(match.group(1))
            key_hex = match.group(2)
            key_byte = int(key_hex[:2], 16)
            # Ajustar índice de rondas
            if 1 <= rounds <= 50:
                cicles_per_round[rounds] +=1
    





plt.figure(figsize=(14, 8))



plt.bar(
    range(51),
    cicles_per_round,
    width=0.7
)
# plt.xlim(-0.5, 255.5)

plt.xlabel("Number of rounds")
plt.ylabel("Total number of cycles")
plt.title("Cycles per round")

plt.xticks(
    range(1,51,1),
    [f"{i}" for i in range(1,51,1)]
)
plt.grid(
    axis='y',
    alpha=0.3
)

min_value=-1
max_value=-1
min_key=0
max_key=0
cicles_bigger_than_0key=0
total_points = 0
for i, value in enumerate(cicles_per_round):

    if value > 0:

        plt.text(
            i,
            value,
            f"{value}",
            ha='center',
            va='bottom',
            fontsize=9,
            rotation=90
        )

    if value >= 461:
        cicles_bigger_than_0key = cicles_bigger_than_0key + 1

    total_points =total_points + value

    if  min_value == -1 or value < min_value:
        min_value = value
        min_key = i

    if  max_value == -1 or value > max_value:
        max_value = value
        max_key = i
    
print(f"Menor cantidad de ciclos: {min_value} en la llave {min_key:02x}")
print(f"Mayor cantidad de ciclos: {max_value} en la llave {max_key:02x}")
print(f"cantidad de ciclos totales: {total_points}")
print(f"cantidad de llaves con ciclos mayores a los de la llave 0: {cicles_bigger_than_0key}")
# print(f"cantidad de puntos fijos totales: {fixed_points}")
plt.tight_layout()
plt.show()