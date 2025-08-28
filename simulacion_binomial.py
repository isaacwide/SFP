import random 
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

def simBinomial():
    theta = 0.2
    histograma = []

    def simple():
        x_n = [random.uniform(0,1) for x in range(100)]
        soles = 0
        for numero in x_n:
            if numero < theta:
                soles += 1
        return soles 

    for i in range(10000):
        histograma.append(simple()) 

    fig, ax = plt.subplots()
    ax.hist(histograma, bins=20, edgecolor="black", density=True)
    ax.set_xlabel("Número de soles (éxitos)")
    ax.set_ylabel("Frecuencia relativa")
    plt.title('Distribución Binomial')
    plt.savefig('static/images/binomial.png')
    plt.close()
    
    promedio = sum(histograma) / len(histograma)
    return histograma, promedio

if __name__ == "__main__":
    simBinomial()
    plt.show()