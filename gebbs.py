import random 
import math 
import numpy as np
import matplotlib.pyplot as plt

def x_y(y):
    u_1 = random.uniform(0,1)
    delta1=math.sqrt(max((4*(y**2))+(12*y)+4+(32*u_1)+(24*y*u_1),0))
    return (-(3*y)-2+delta1)/2
 
def y_x(x):
    u_1 = random.uniform(0,1)
    delta2 = math.sqrt(max((x**2) + (2*x) + 1 + (6*u_1*x) + (15*x),0))
    return (-(2*x) - 2 + (2*delta2)) / 3

def gebbs(n):
    x0 = random.randint(0,10)
    y0 = random.randint(0,10)
    samples = [(x0,y0)]
    for i in range(n):
        x_n=x_y(samples[i][1])
        y_n=y_x(samples[i][0])
        samples.append((x_n,y_n))
    return samples

if __name__ == "__main__":
    n = 1000
    samples = gebbs(n)

    fig = plt.figure()
    ax = plt.axes(projection='3d')

    z = [1 for _ in samples]  
    x = [xs[1] for xs in samples]
    y = [xs[0] for xs in samples]

    ax.scatter3D(x, y, z, color='blue', marker='o') 

    plt.show()