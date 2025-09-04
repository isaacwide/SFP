import random
import numpy as np

def simMultinomial(n, rangos, uniforme):
    if uniforme:
        probabilidades = [1/rangos] * rangos
    else:
       
        probabilidades = np.random.dirichlet(np.ones(rangos), size=1)[0]

    histograma = [0] * rangos

    muestras = [random.uniform(0,1) for _ in range(n)]
    intervalos = [0] + list(np.cumsum(probabilidades))

    for u in muestras:  # <-- corregido nombre
        for i in range(len(intervalos)-1):
            if intervalos[i] <= u < intervalos[i+1]:
                histograma[i] += 1
                break

    print("Probabilidades:", probabilidades)
    print("Histograma:", histograma)
    return histograma
