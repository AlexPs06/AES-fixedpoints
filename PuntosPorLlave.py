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

density = np.zeros((256), dtype=int)


for i in range(16):
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
            
            # Como la llave es:
            # 010101...
            # 020202...
            # etc.
            # basta tomar el primer byte
            key_byte = int(key_hex[:2], 16)
            # Ajustar índice de rondas
            if 1 <= rounds <= 50:
                density[key_byte] += 1
        # if j>1000:
            # break
    # break
# plt.figure(figsize=(16,8))

# plt.bar(
#     range(256),
#     density
# )

# plt.yscale('log')

# plt.xlabel("Key Byte")
# plt.ylabel("Cantidad de puntos fijos")
# plt.title("Puntos fijos por llave (escala log)")

# plt.xticks(
#     range(0,256,1),
#     [f"{i:02x}" for i in range(0,256,1)]
# )

# plt.show()



plt.figure(figsize=(32,32))

plt.bar(
    range(256),
    density
)

plt.xlabel("Key Byte")
plt.ylabel("Cantidad de ciclos")
plt.title("Ciclos por llave")

plt.xticks(
    range(0,256,16),
    [f"{i:02x}" for i in range(0,256,16)]
)


min_value=-1
min_key=0
for i, value in enumerate(density):

    if value > 0:

        plt.text(
            i,
            value,
            f"{value}",
            ha='center',
            va='bottom',
            fontsize=6,
            rotation=90
        )
    if  min_value == -1 or value < min_value:
        min_value = value
        min_key = i
    
print(f"Menor cantidad de ciclos: {min_value} en la llave {min_key:02x}")
plt.show()