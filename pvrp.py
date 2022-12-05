from pulp import *
import numpy as np
T=(1,2)
Lambda = ([1],[2],[1,2])
LambdaI=([2],[0,1],[0,1])
c=([0,5,7,5,0],
     [5,0,5,7,5],
     [7,5,0,5,7],
     [5,7,5,0,5],
     [0,5,7,5,0])
d=(10,10,10)
a=([1,0],[0,1],[1,1])
stringS=[]
currentSolution = 0
maxRecord = 40
maxIter = 80
p = 0.7
fi = 0
runTime = 0
maxTime = 0
neighbourhoodSize = 0
H = LpVariable("maximum amount of demand serviced on a day", 0, None, LpInteger)
minImprove = 0.0005
maxDeviation = 0.0005

numberOfCustomers = 3

if(numberOfCustomers <= 50):
    neighbourhoodSize = numberOfCustomers - 1
    maxTime = 400
elif(numberOfCustomers <= 100):
    neighbourhoodSize = numberOfCustomers - 1
    maxTime = 900
else:
    neighbourhoodSize = 10
    maxTime = 900

recCntr = 0
iterCntr = 0


def generate_initial():
    problem = pulp.LpProblem("PVRP", LpMinimize)
    u = [[pulp.LpVariable("u_%s_%s"%(i,k), cat="Binary") for k in LambdaI[i]]for i in range(numberOfCustomers)] 
    problem+=H
    
    for i in range(numberOfCustomers):
        problem+=pulp.lpSum(u[i][k] for k in range(len(LambdaI[i])))==1
    
    
    for t in range(len(T)):
        problem+=pulp.lpSum(a[ki][t]*d[i]*u[i][k] for i in range (numberOfCustomers) for ki, k in zip(LambdaI[i], range(len(LambdaI[i]))) )<=H
    
    if problem.solve() == 1:
        return u
    
S=generate_initial()

for v in range(len(S)):
    for vv in range(len(S[v])):
        stringS.append(str(S[v][vv]) + "_" + str(int(S[v][vv].varValue)))

print(stringS)

ik=[0]*4

for vvv in range(len(stringS)):
    x=stringS[vvv].split("_")
    if(int(x[3]) ==1):
        ik[int(x[1])]=int(x[2])
ik[3]=2

order=([0],[0])
for i in range(numberOfCustomers):
    for t in T:
        if t in Lambda[ik[i]]:
            order[t-1].append(i+1)  
for t in T:
    order[t-1].append(numberOfCustomers+1)

def IIP():
    
    problem = pulp.LpProblem("PVRP", LpMaximize)
    y = [[pulp.LpVariable("y_%s_%s"%(i+1,t), cat="Binary") for t in T if t  in Lambda[ik[i]]]for i in range(numberOfCustomers)] 
    x = [[[pulp.LpVariable("x_%s_%s_%s"%(i+1,j+1,t), cat="Binary")for t in T if t in Lambda[ik[j]] and t not in Lambda[ik[i]]]for j in range(numberOfCustomers+1) if j is not i]for i in range(numberOfCustomers)] 
    ys=pulp.lpSum(((c[order[Lambda[ik[i-1]][ty]-1][order[Lambda[ik[i-1]][ty]-1].index(i)-1]][i]+c[i][order[Lambda[ik[i-1]][ty]-1][order[Lambda[ik[i-1]][ty]-1].index(i)+1]]-c[order[Lambda[ik[i-1]][ty]-1][order[Lambda[ik[i-1]][ty]-1].index(i)-1]][order[Lambda[ik[i-1]][ty]-1][order[Lambda[ik[i-1]][ty]-1].index(i)+1]])*
                   y[i-1][ty])for i in range(1,numberOfCustomers+1)for ty in range(len(y[i-1]))) 
    
    xs= pulp.lpSum(((c[order[int(x[i-1][j-1][tx].name.split("_")[3])-1][order[int(x[i-1][j-1][tx].name.split("_")[3])-1].index(int(x[i-1][j-1][tx].name.split("_")[2]))-1]][int(x[i-1][j-1][tx].name.split("_")[1])]+c[int(x[i-1][j-1][tx].name.split("_")[1])][int(x[i-1][j-1][tx].name.split("_")[2]) ]-c[order[int(x[i-1][j-1][tx].name.split("_")[3])-1][order[int(x[i-1][j-1][tx].name.split("_")[3])-1].index(int(x[i-1][j-1][tx].name.split("_")[2]))-1]][int(x[i-1][j-1][tx].name.split("_")[2])])*
                    x[i-1][j-1][tx])for i in range(1,numberOfCustomers+1)for j in range(1,numberOfCustomers+1)  for tx in range(len(x[i-1][j-1])))

    h=order[int(x[3-1][3-1][0].name.split("_")[3])-1][order[int(x[3-1][3-1][0].name.split("_")[3])-1].index(int(x[3-1][3-1][0].name.split("_")[2]))-1]
    problem += ys-xs   
    print()
 
IIP()
print()   
# https://developers.google.com/optimization/routing/vrp