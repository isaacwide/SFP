import random
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

def simBernoulli(theta, n):
    x_n = [random.uniform(0, 1) for x in range(n)]
    secuencia = []  # Almacena la secuencia de resultados
    soles = 0 
    aguilas = 0 

    for numero in x_n:
        if numero < theta:
            aguilas += 1
            secuencia.append(0)  # aguila
        else:
            soles += 1
            secuencia.append(1)  #sol

    return soles, aguilas, secuencia