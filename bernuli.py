import random
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

def simBernoulli():
    theta = 0.7
    x_n = [random.uniform(0,1) for x in range(100)]

    soles = 0 
    aguilas = 0 

    for numero in x_n:
        if numero < theta:
            aguilas += 1
        else:
            soles += 1 

    print("total de soles = ", soles)
    print("total de aguilas = ", aguilas)

    par = [soles, aguilas]
    fig, ax = plt.subplots()
    ax.bar(x=range(len(par)), height=par)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Soles', 'Águilas'])
    plt.title('Distribución de Bernoulli')
    plt.savefig('static/images/bernoulli.png')
    plt.close()
    
    return soles, aguilas

if __name__ == "__main__":
    simBernoulli()
    plt.show()




