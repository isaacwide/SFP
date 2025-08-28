import random 
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

def simBinomial(theta,lanzamientos,repeticiones):
    histograma = []

    def simple():
        x_n = [random.uniform(0,1) for x in range(lanzamientos)]
        soles = 0
        for numero in x_n:
            if numero < theta:
                soles += 1
        return soles 

    for i in range(repeticiones):
        histograma.append(simple()) 
        
    promedio = sum(histograma) / len(histograma)
    return histograma, promedio
