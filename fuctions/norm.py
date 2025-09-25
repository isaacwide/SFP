import random
import math
import matplotlib.pyplot as plt

def normalEstandar(n, miu, sigma):
    u1 = [random.uniform(0,1) for x in range(n)]
    u2 = [random.uniform(0,1) for x in range(n)]
    x = []
    for i in range(n):
        aux = math.sqrt(2*(math.log(1/u1[i])))*math.cos(6.283*u2[i])
        aux2 = sigma*aux + miu  
        x.append(aux2)

    return x  