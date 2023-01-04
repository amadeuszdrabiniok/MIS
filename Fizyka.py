from random import seed
from random import randint
import matplotlib.pyplot as plt
import numpy as np

def plot_points(A):
    x = list(range(len(A)))
    y = A

    plt.plot(x, y)
    plt.show()

def is_same(x,xs):
    if x==xs:
        xs=randint(0,1000)
        xs=is_same(x,xs)
    else:
        return xs
seed(1)
N  = np.random.uniform(0,1,1000)
d=0.2
u=0.5
for i in range(10000):
    plot_points(N)
    x=randint(0,1000)
    xs=randint(0,1000)
    xs=is_same(x,xs)
    if abs(N[x]-N[xs])<d:
        N[x]=N[x]+u*(N[xs]-N[x])
        N[xs]=N[xs]+u*(N[x]-N[xs])
