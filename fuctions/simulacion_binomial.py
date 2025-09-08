import random 
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

def simBinomial(theta, lanzamientos, repeticiones):
    histograma = []
    secuencia_completa = []

    def simple():
        x_n = [random.uniform(0,1) for x in range(lanzamientos)]
        soles = 0
        for numero in x_n:
            if numero < theta:
                soles += 1
        return soles, x_n 

    for i in range(repeticiones):
        soles, lanzamientos_exp = simple()
        histograma.append(soles)
        secuencia_completa.extend(lanzamientos_exp) 
        
    promedio = sum(histograma) / len(histograma)
    return histograma, promedio, secuencia_completa 