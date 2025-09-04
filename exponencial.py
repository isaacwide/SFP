import random
import matplotlib.pyplot as plt
import math

lmbda = 0.5
n = 100

x_n = [-math.log(1 - random.uniform(0,1)) / lmbda for _ in range(n)]

umbral = 1.0  # cualquier valor que tú decidas
soles = 0
aguilas = 0

for numero in x_n:
    if numero < umbral:
        aguilas += 1
    else:
        soles += 1

print("total de soles =", soles)
print("total de aguilas =", aguilas)

par = [soles, aguilas]
fig, ax = plt.subplots()
ax.bar(x=range(len(par)), height=par)
plt.show()
