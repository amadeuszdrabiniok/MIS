from pulp import *
import numpy as np

def generate_initial(Lambda, LambdaI, numberOfCustomers):
    H = LpVariable("maximum amount of demand serviced on a day", 0, None, LpInteger)
    problem = pulp.LpProblem("PVRP", LpMinimize)
    u = [[pulp.LpVariable("u_%s_%s"%(i,k), cat="Binary") for k in LambdaI[i]]for i in range(1, numberOfCustomers+1)]
    problem+=H

    for i in range(1, numberOfCustomers+1):
        problem+=pulp.lpSum(u[i][k] for k in range(len(LambdaI[i])))==1

    for t in days:
        problem+=pulp.lpSum(a[ki][t]*d[i]*u[i][k] for i in range (numberOfCustomers) for ki, k in Lambda) <=H

    if problem.solve() == 1:
        return u
