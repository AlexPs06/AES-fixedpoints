import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from collections import defaultdict


# =========================
# Leer archivo
# =========================

# =========================
# Matriz de densidad
# Filas  -> llaves (0-255)
# Columnas -> rondas (1-50)
# =========================

density = np.zeros((256, 50), dtype=int)


fixed_points = defaultdict(set)

for i in range(32):
    filename = f"fixed-point-thread-{i}.txt"
    # print(f"Procesando {filename}...")
    with open(filename, "r") as f:
        lines = f.readlines()

    # =========================
    # Parsear líneas
    # =========================
    #Fixed Point: 12dc340112dc340112dc340112dc3401 | Rounds: 47 | Key: 00000000000000000000000000000000

    pattern = r"Fixed Point:\s*([0-9a-fA-F]+)\s*\|\s*Rounds:\s*(\d+)\s*\|\s*Key:\s*([0-9a-fA-F]+)"
    j=0

    for line in lines:
        j += 1
        line = line.strip()
        match = re.search(pattern, line)

        if match:

            fixed_point = match.group(1)
            rounds = int(match.group(2))
            key_hex = match.group(3)
            
            key_byte = int(key_hex[:2], 16)
            fixed_points[key_byte].add(fixed_point)



shared = fixed_points[0x00] & fixed_points[0x01]
print(len(shared))


intersection_matrix = np.zeros((256,256), dtype=int)
max_points_interseccion = 0
save_shared = shared
i_temp = 0
j_temp = 0

for i in range(256):

    for j in range(256):

        shared = fixed_points[i] & fixed_points[j]
        intersection_matrix[i,j] = len(shared)
        if (max_points_interseccion< len(shared)):
            max_points_interseccion=len(shared)
            print("i: ", i, "j: ", j, "shared_size: ", len(shared))
            print("shared_size: ", shared)




plt.figure(figsize=(14,12))
np.fill_diagonal(intersection_matrix, 0)

im = plt.imshow(
    intersection_matrix,
    origin='lower',
    cmap='turbo',
    aspect='auto',
    norm=LogNorm()
)

plt.colorbar(
    im,
    label='Puntos fijos compartidos'
)

plt.xlabel("Key")
plt.ylabel("Key")


ticks = np.arange(0,256,16)

labels = [f"{i:02x}" for i in ticks]

plt.xticks(ticks, labels)
plt.yticks(ticks, labels)

plt.title(
    "Intersección de puntos fijos entre llaves"
)


plt.tight_layout()
plt.show()




# im = plt.imshow(
#     intersection_matrix + 1,
#     origin='lower',
#     cmap='turbo',
#     norm=LogNorm()
# )






# fig, ax = plt.subplots(figsize=(14,12))
# np.fill_diagonal(intersection_matrix, 0)

# # Fondo
# # fig.patch.set_facecolor('white')   # fondo exterior
# # ax.set_facecolor('black')          # fondo interior

# # Heatmap
# im = ax.imshow(
#     intersection_matrix,
#     origin='lower',
#     cmap='turbo',
#     norm=LogNorm()
# )

# # Barra lateral
# cbar = plt.colorbar(im)
# cbar.set_label('Puntos fijos compartidos')

# # Ejes
# ticks = np.arange(0,256,16)

# labels = [f"{i:02x}" for i in ticks]

# ax.set_xticks(ticks)
# ax.set_yticks(ticks)

# ax.set_xticklabels(labels)
# ax.set_yticklabels(labels)

# # Texto blanco
# ax.xaxis.label.set_color('white')
# ax.yaxis.label.set_color('white')

# ax.tick_params(colors='white')

# plt.title(
#     "Intersección de puntos fijos entre llaves",
#     color='white'
# )

# plt.show()

