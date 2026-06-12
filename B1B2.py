import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from collections import defaultdict
from matplotlib.colors import Normalize


# =========================
# Leer archivo
# =========================

# =========================
# Matriz de densidad
# Filas  -> llaves (0-255)
# Columnas -> rondas (1-50)
# =========================

density = np.zeros((256, 50), dtype=int)


fixed_points = defaultdict(lambda: defaultdict(list))
j=0

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

    for line in lines:
        j += 1
        line = line.strip()
        match = re.search(pattern, line)

        if match:

            fixed_point = match.group(1)
            rounds = int(match.group(2))
            key_hex = match.group(3)
            # Como la llave es:
            # 010101...
            # 020202...
            # etc.
            # basta tomar el primer byte            
            key_byte = int(key_hex[:2], 16)

            # fixed_points_dict[fixed_point].append((key_byte, rounds))
            fixed_points[fixed_point][key_byte].append(rounds)






print(j)
j=0
max_keys = 0
max_fixed_points = 0
repeat_cyles = 0

B1B2 = np.zeros((256, 256), dtype=int)

for fp, keys in fixed_points.items():
    if len(keys) > max_keys:
        max_keys = len(keys)
        max_fixed_points = fp
    if len(keys) > 1:
        repeat_cyles=repeat_cyles+1 
    
    if len(keys) > 1:
        B1B2[int(fp[0:2],16) ][ int(fp[2:4],16) ] +=len(keys)   




# ==========================================
# Preparar datos
# ==========================================

x = []
y = []
values = []

for b1 in range(256):
    for b2 in range(256):

        value = B1B2[b1][b2]

        if value > 0:
            # print(value)
            x.append(b1)
            y.append(b2)
            values.append(value)



# ==========================================
# Figura
# ==========================================

plt.figure(figsize=(14,12))

# ==========================================
# Scatter/Bubble Plot
# ==========================================

scatter = plt.scatter(
    x,
    y,

    # tamaño del círculo
    # s=[20 + v*5 for v in values],
    s=25,
    # color asociado al valor
    c=values,

    cmap='turbo',   # azul -> rojo

    # norm=LogNorm(),

    alpha=0.9
)

# ==========================================
# Barra de color
# ==========================================

cbar = plt.colorbar(scatter)

cbar.set_label(
    "Cantidad de ocurrencias"
)

# ==========================================
# Ejes
# ==========================================

ticks = np.arange(0,256,16)

labels = [f"{i:02x}" for i in ticks]

plt.xticks(ticks, labels)
plt.yticks(ticks, labels)

plt.xlabel("B1")
plt.ylabel("B2")

plt.title(
    "Distribución B1-B2 de puntos fijos compartidos"
)

plt.grid(alpha=0.2)

plt.tight_layout()
plt.show()