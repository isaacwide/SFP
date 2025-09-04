#distibucion de una funcion normal estandad sin parametros adicionales 
import random
import math
import matplotlib.pyplot as plt

def normalEstandar(n,miu,sigma):
    u1=[random.uniform(0,1) for x in range(n)]
    u2=[random.uniform(0,1) for x in range(n)]
    x=[]
    for i in range(n):
        aux = math.sqrt(2*(math.log(1/u1[i])))*math.cos(6.283*u2[i])
        aux2=sigma*aux+miu  
        x.append(aux2)

    return x
if __name__ == "__main__":
    #n es el numero de repeticiones de esta simulacion
    n=10000
    miu=30
    sigma=5
    valores = normalEstandar(n,miu,sigma)

    fig, ax = plt.subplots()
    ax.hist(valores, bins=50, edgecolor="black", density=True)
    ax.set_xlabel("Valores simulados (N(0,1))")
    ax.set_ylabel("Frecuencia relativa")
    plt.show()
