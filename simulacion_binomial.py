import random 
import matplotlib.pyplot as plt
#sumulacionde una funcionde destribucion binomial 

theta = 0.5

#numero de repeticiones 
histograma = []

def simple():
    x_n = [random.uniform(0,1) for x in range(100)]
    soles = 0
    for numero in x_n:
        if numero > 0 and numero < theta :
            soles += 1
    pass
    return soles 

for i in range(100000):
    histograma.append(simple()) 
    

#grafico de barras 
fig,ax = plt.subplots()
ax.bar(x=range(len(histograma)),height=histograma)
plt.savefig('figure.png')
plt.show()