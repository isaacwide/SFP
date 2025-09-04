import random
import numpy as np

# Generar probabilidades aleatorias que sumen 1
probabilidades = np.random.dirichlet(np.ones(6), size=1)[0]
intervalos_aleatorios = [0] + list(np.cumsum(probabilidades))

histograma = [0]*6
n_k = [random.uniform(0,1) for _ in range(10000)]

for n in n_k:
    for i in range(6):
        if intervalos_aleatorios[i] <= n < intervalos_aleatorios[i+1]:
            histograma[i] += 1
            break
print("Histograma:", histograma)