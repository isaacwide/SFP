import random
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

def simMultinomial():
    rangos = [0.166*(x+1) for x in range(5)]
    histograma = [0]*6

    n_k = [random.uniform(0,1) for _ in range(10000)]

    for n in n_k:
        if n >= 0 and n < rangos[0]:
            histograma[0] += 1
        elif n >= rangos[0] and n < rangos[1]:
            histograma[1] += 1
        elif n >= rangos[1] and n < rangos[2]:
            histograma[2] += 1
        elif n >= rangos[2] and n < rangos[3]:
            histograma[3] += 1
        elif n >= rangos[3] and n < rangos[4]:
            histograma[4] += 1
        else:
            histograma[5] += 1
    
    print(histograma)
    print(sum(histograma))
    print(rangos)
    
    fig, ax = plt.subplots()
    ax.bar(x=range(len(histograma)), height=histograma)
    ax.set_xlabel('Cara del dado')
    ax.set_ylabel('Frecuencia')
    ax.set_xticks(range(6))
    ax.set_xticklabels([f'Cara {i+1}' for i in range(6)])
    plt.title('Distribución Multinomial (Dado)')
    plt.savefig('static/images/multinomial.png')
    plt.close()
    
    return histograma

if __name__ == "__main__":
    simMultinomial()
    plt.show()