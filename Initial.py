from pulp import *
import numpy as np

def generate_initial(Lambda, LambdaI, numberOfCustomers,a, T, d):
    print(Lambda)
    print(LambdaI)
    print(numberOfCustomers)
    print(a)
    print(T)
    print(d)
    H = LpVariable("maximum amount of demand serviced on a day", 0, None, LpInteger)
    problem = pulp.LpProblem("PVRP", LpMinimize)
    u = [[pulp.LpVariable("u_%s_%s"%(i,k), cat="Binary") for k in LambdaI[i]]for i in range(numberOfCustomers)]
    problem+=H

    for i in range(numberOfCustomers):
        problem+=pulp.lpSum(u[i][k] for k in range(len(LambdaI[i])))==1


    for t in range(len(T)):
        problem+=pulp.lpSum(a[ki][t]*d[i]*u[i][k] for i in range (numberOfCustomers) for ki, k in zip(LambdaI[i], range(len(LambdaI[i]))) )<=H

    if problem.solve() == 1:
        return u
