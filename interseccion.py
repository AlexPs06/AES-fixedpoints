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
for fp, keys in fixed_points.items():
    if len(keys) > max_keys:
        max_keys = len(keys)
        max_fixed_points = fp
    if len(keys) > 1:
        repeat_cyles=repeat_cyles+1 
    # if len(keys) > 1 and ((fp[0:2] != fp[4:6] ) or (fp[2:4] != fp[6:8] )):
        # j += len(keys)
        # print(f"Punto fijo: {fp}")
        # print(f"Punto fijo: {fp[0:2]}")
        # print(f"Punto fijo: {fp[2:4]}")
        # print(f"Punto fijo: {fp[4:6]}")
        # print(f"Punto fijo: {fp[6:8]}")
        # print(f"Aparece en {len(keys)} llaves")
        # print(f"Aparece en {keys} llaves")
        # exit(0)

# print(f"El punto fijo con más llaves es: {max_fixed_points} con {max_keys} llaves")
# print(fixed_points[max_fixed_points])


# print(f"Numero total de ciclos que no se repiten encontrados: {len(fixed_points)-repeat_cyles}")
# print(f"Numero total de ciclos que se repiten: {repeat_cyles}")

from collections import defaultdict

repetition_distribution = defaultdict(int)

for fp, keys in fixed_points.items():

    num_keys = len(keys)
    if len(keys)>1:
        repetition_distribution[num_keys] += 1


x = sorted(repetition_distribution.keys())

y = [repetition_distribution[k] for k in x]

import matplotlib.pyplot as plt

plt.figure(figsize=(12,6))

# bars = plt.bar(
    # x,
    # y,
    # width=0.8,
    # edgecolor='black'
# )

plots = plt.plot(
    x,
    y,
    marker='o',      # puntos
    linestyle='-',   # unir puntos
    linewidth=2,
    markersize=6
)

plt.xticks(
    range(0,70,1),
    [f"{i}" for i in range(0,70,1)]
)

plt.xlabel("Número de llaves compartiendo el punto fijo")
plt.ylabel("Cantidad de puntos fijos")

plt.title(
    "Distribución de puntos fijos compartidos"
)

plt.grid(
    axis='y',
    alpha=0.3
)


for i, value in enumerate(repetition_distribution):

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

plt.tight_layout()
plt.show()




# plt.figure(figsize=(16,10))

# scatter = plt.scatter(
#     x,
#     y,
#     s=[20*s for s in sizes],
#     c=sizes,
#     alpha=0.7,
#     # norm=LogNorm(),

# )

# plt.colorbar(
#     scatter,
#     label="Peso acumulado"
# )

# plt.xlabel("Key Byte")
# plt.ylabel("Rounds")

# plt.xticks(
#     range(0,256,8),
#     [f"{i:02x}" for i in range(0,256,8)]
# )

# plt.yticks(
#     range(0,50,1),
#     [f"{i}" for i in range(0,50,1)]
# )

# plt.title(
#     "Regiones donde los puntos fijos se repiten"
# )

# plt.grid(True, alpha=0.3)

# plt.tight_layout()
# plt.show()



