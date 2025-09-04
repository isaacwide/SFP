import random
import matplotlib.pyplot as plt
#multinomial 
# caras de un dado 
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
fig,ax = plt.subplots() 
ax.bar(x=range(len(histograma)),height=histograma)  
plt.show()


