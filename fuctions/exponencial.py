import random
import math
import matplotlib
matplotlib.use('Agg')

import random
import math
import matplotlib.pyplot as plt

def simExponencial(lmbda, n):
    x_n = [-math.log(1 - random.uniform(0,1)) / lmbda for _ in range(n)]
    return x_n

