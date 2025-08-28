import random
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

def simBernoulli(theta,n):
    x_n = [random.uniform(0,1) for x in range(n)]

    soles = 0 
    aguilas = 0 

    for numero in x_n:
        if numero < theta:
            aguilas += 1
        else:
            soles += 1 

    return soles, aguilas





