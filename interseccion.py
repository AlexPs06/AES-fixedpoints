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

for i in range(16):
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
            # Como la llave es:
            # 010101...
            # 020202...
            # etc.
            # basta tomar el primer byte            
            key_byte = int(key_hex[:2], 16)

            # fixed_points_dict[fixed_point].append((key_byte, rounds))
            fixed_points[fixed_point][key_byte].append(rounds)
            # print(f"Fixed Point: {fixed_point}, Rondas: {rounds}, Llave: {key_hex}")
            

            # if 1 <= rounds <= 50:
            #     density[key_byte, rounds - 1] += 1
# print(fixed_points)






max_keys = 0
max_fixed_points = 0
for fp, keys in fixed_points.items():

    if len(keys) > max_keys:
        max_keys = len(keys)
        max_fixed_points = fp
    if len(keys) >= 4:

        print(f"Punto fijo: {fp}")
        print(f"Aparece en {len(keys)} llaves")

# print(f"El punto fijo con más llaves es: {max_fixed_points} con {max_keys} llaves")
# print(fixed_points[max_fixed_points])



exit(0)




metric = defaultdict(int)

for fp, keys in fixed_points.items():

    # número de llaves distintas que generan este FP
    num_keys = len(keys)

   

    # ignorar puntos fijos exclusivos
    if num_keys <= 1:
        continue
    
    # print(f"Punto fijo: {fp} aparece en {num_keys} llaves distintas")
    # peso asociado a este FP
    # weight = num_keys - 1

    for key_byte, rounds_list in keys.items():
        # key_value = int(key_byte, 16)

        for rnd in rounds_list:

            metric[(key_byte, rnd)] += 1
            # print(f"  - Llave: {key_byte:02x}, Rondas: {rnd}, Peso acumulado: {metric[(key_byte, rnd)]}")
    
    # exit(0)
best_pair = max(metric, key=metric.get)

best_key, best_round = best_pair

print(f"Key: {best_key:02x}")
print(f"Round: {best_round}")
print(f"Score: {metric[best_pair]}")

x = []
y = []
sizes = []

for (key_value, rnd), score in metric.items():

    x.append(key_value)
    y.append(rnd)

    sizes.append(score)



plt.figure(figsize=(16,10))

scatter = plt.scatter(
    x,
    y,
    s=[20*s for s in sizes],
    c=sizes,
    alpha=0.7,
    norm=LogNorm(),

)

plt.colorbar(
    scatter,
    label="Peso acumulado"
)

plt.xlabel("Key Byte")
plt.ylabel("Rounds")

plt.xticks(
    range(0,256,16),
    [f"{i:02x}" for i in range(0,256,16)]
)

plt.title(
    "Regiones donde los puntos fijos se repiten"
)

plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()



