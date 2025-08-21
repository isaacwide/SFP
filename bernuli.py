import random
#funcion de bernulli 
theta = 0.7
x_n = [random.uniform(0,1) for x in range(100)]

soles = 0 
aguilas =0 

for numero in x_n:
    if numero > 0 and numero < theta :
        aguilas += 1
    else:
        soles += 1 

print("total de soles = ",soles)
print("total de aguilas = ",aguilas)






