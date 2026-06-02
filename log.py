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

density = np.zeros((256, 50), dtype=int)


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
                density[key_byte, rounds - 1] += 1
        # if j>1000:
            # break
    # break
    
# =========================
# Graficar Heatmap
# =========================
plt.figure(figsize=(14, 8))

#2. Configurar la normalización logarítmica
# linthresh=1 indica que entre 0 y 1 la escala será lineal para evitar error con el log(0)
# log_norm = mcolors.SymLogNorm(linthresh=1, vmin=0, vmax=density.max(), base=10)
log_norm = mcolors.LogNorm(vmin=1, vmax=density.max())

im = plt.imshow(
    density,
    aspect='auto',
    origin='lower',
    cmap='turbo',
    norm=log_norm  # <-- 3. Aplicar la norma aquí
)

# El colorbar tomará automáticamente la escala de 'im'
plt.colorbar(im, label='Cantidad de puntos fijos (Escala Log)')

plt.xlabel('Rounds')
plt.ylabel('Key Byte Value')

# Etiquetas de rondas
plt.xticks(
    ticks=np.arange(0, 50, 1),
    labels=np.arange(1, 51, 1)
)

# Etiquetas de llaves
plt.yticks(
    ticks=np.arange(0, 256, 16),
    labels=[hex(i) for i in range(0, 256, 16)]
)



# ==========================================
# Texto dentro de cada celda
# ==========================================

# for y in range(256):
#     for x in range(50):

#         value = density[y, x]

#         # Mostrar solo si hay algo
#         if value >= 0:

#             plt.text(
#                 x,
#                 y,
#                 f"{value}",   # hexadecimal
#                 ha='center',
#                 va='center',
#                 fontsize=10,
#                 color='white'
#             )


plt.title('Densidad de puntos fijos por llave y rondas')

plt.tight_layout()
plt.show()