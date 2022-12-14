from pulp import *
import numpy as np

T=(1,2)
LambdaA=(0,1,2)
Lambda = ([1],[2],[1,2])
LambdaI=([2],[0,1],[0,1])
c=([0,5,7,5,0],
     [5,0,5,7,5],
     [7,5,0,5,7],
     [5,7,5,0,5],
     [0,5,7,5,0])
d=(10,10,10)
a=([0,1],[1,0],[1,1])
stringS=[]
currentSolution = 0
maxRecord = 40
maxIter = 80
p = 0.7
fi = 0
runTime = 0
maxTime = 0
neighbourhoodSize = 0

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
    Q=[0]*len(T)
    for i in T:
        b=[d[order[i-1][k]-1] for k in range(1, len(order[i-1])-1)]
        Q[i-1]=sum(b)
    problem = pulp.LpProblem("PVRP", LpMaximize)
    y = [[pulp.LpVariable("y_%s_%s"%(i+1,t), cat="Binary") for t in T if t  in Lambda[ik[i]]]for i in range(numberOfCustomers)] 
    x = [[[pulp.LpVariable("x_%s_%s_%s"%(i+1,j+1,t), cat="Binary")for t in T if t in Lambda[ik[j]] and t not in Lambda[ik[i]]]for j in range(numberOfCustomers+1) if j is not i]for i in range(numberOfCustomers)] 
    w = [[pulp.LpVariable("w_%s_%s"%(i+1,k+1), cat="Binary")for k in LambdaA if k in LambdaI[i] and k is not ik[i]] for i in range(numberOfCustomers)] 
    ys=pulp.lpSum(((c[order[Lambda[ik[i-1]][ty]-1][order[Lambda[ik[i-1]][ty]-1].index(i)-1]][i]+c[i][order[Lambda[ik[i-1]][ty]-1][order[Lambda[ik[i-1]][ty]-1].index(i)+1]]-c[order[Lambda[ik[i-1]][ty]-1][order[Lambda[ik[i-1]][ty]-1].index(i)-1]][order[Lambda[ik[i-1]][ty]-1][order[Lambda[ik[i-1]][ty]-1].index(i)+1]])*
                y[i-1][ty])for i in range(1,numberOfCustomers+1)for ty in range(len(y[i-1]))) 
    
    xs= pulp.lpSum(((c[order[int(x[i-1][j-1][tx].name.split("_")[3])-1][order[int(x[i-1][j-1][tx].name.split("_")[3])-1].index(int(x[i-1][j-1][tx].name.split("_")[2]))-1]][int(x[i-1][j-1][tx].name.split("_")[1])]+c[int(x[i-1][j-1][tx].name.split("_")[1])][int(x[i-1][j-1][tx].name.split("_")[2]) ]-c[order[int(x[i-1][j-1][tx].name.split("_")[3])-1][order[int(x[i-1][j-1][tx].name.split("_")[3])-1].index(int(x[i-1][j-1][tx].name.split("_")[2]))-1]][int(x[i-1][j-1][tx].name.split("_")[2])])*
                    x[i-1][j-1][tx])for i in range(1,numberOfCustomers+1)for j in range(1,numberOfCustomers+1)  for tx in range(len(x[i-1][j-1])))

    problem += ys-xs   
    
    for i in range(numberOfCustomers):
        problem+=pulp.lpSum(y[i][t] for t in range(len(y[i]))) == pulp.lpSum(x[i][j][t] for j in range(numberOfCustomers) for t in range(len(x[i][j])))
        
    for i in range(numberOfCustomers):
        problem+=pulp.lpSum(x[i][j][t] for j in range(numberOfCustomers) for t in range(len(x[i][j]))) <= pulp.lpSum(w[i][k] for k in range(len(w[i])))
        
    for i in range(numberOfCustomers):
        for t in T:
            if t in range(len(y[i])+1):
                problem+=pulp.lpSum(x[i][j][t-1] for j in range(numberOfCustomers) for t in range(len(x[i][j])))<= y[i][t-1]

    for i in range(numberOfCustomers):
        for k in range(len(w[i])):
                problem+=pulp.lpSum(x[i][j][t] for j in range(numberOfCustomers) for t in range(len(x[i][j])))>=w[i][k]
                
    for i in range(numberOfCustomers):
        for k in range(len(w[i])):
            for t in range(len(y[i])):
                    problem+=pulp.lpSum(x[i][j][t] for j in range(numberOfCustomers) for t in range(len(x[i][j])))+1-y[i][t]>=w[i][k]
    
    for i in range(numberOfCustomers):
        for t in range(len(y[i])): 
            for r in T:  
                if len(x[i][0])>0:         
                    problem+=pulp.lpSum(x[i][j][t]* d[i] for j in range(numberOfCustomers))-pulp.lpSum(d[i] * y[i][t])<=Q[r-1]
                          
    idontwanttodothisanymore=[]
                
    for i in range(numberOfCustomers):
        for t in T:
            if t in range(len(y[i])+1):
                y[i][t-1].name.split('_')
                for hehe in x:
                    if len(hehe[0]) != 0:
                        for kk in range(len(hehe)):
                            if hehe[kk][0].name.split('_')[-1] == y[i][t-1].name.split('_')[-1] and hehe[kk][0].name.split('_')[-2] == y[i][t-2].name.split('_')[-2] :
                                idontwanttodothisanymore.append(hehe[kk])
                problem+=idontwanttodothisanymore+y[i][t-1]<= 1
                idontwanttodothisanymore.clear()
    
    for i in range(numberOfCustomers):
        for t in T:
            if t in range(len(y[i])+1):
                y[i][t-1].name.split('_')
                for hehe in x:
                    if len(hehe[0]) != 0:
                        for kk in range(len(hehe)):
                            if hehe[kk][0].name.split('_')[-1] == y[i][t-1].name.split('_')[-1] and hehe[kk][0].name.split('_')[-2] == y[i][t-2].name.split('_')[-2] :
                                idontwanttodothisanymore.append(hehe[kk])
                if order[int(y[i][t-1].name.split('_')[-1])-1][order[int(y[i][t-1].name.split('_')[-1])-1].index(i+1)-1]-1 < len(y):
                    if int(y[i][t-1].name.split('_')[-1])-1 < len(y[order[int(y[i][t-1].name.split('_')[-1])-1][order[int(y[i][t-1].name.split('_')[-1])-1].index(i+1)-1]-1]):
                        if order[int(y[i][t-1].name.split('_')[-1])-1][order[int(y[i][t-1].name.split('_')[-1])-1].index(i+1)-1] is not 0:
                            problem+=idontwanttodothisanymore+y[order[int(y[i][t-1].name.split('_')[-1])-1][order[int(y[i][t-1].name.split('_')[-1])-1].index(i+1)-1]-1][int(y[i][t-1].name.split('_')[-1])-1]<= 1
            idontwanttodothisanymore.clear()
                
    
    
    for i in range(1,numberOfCustomers):
        for t in T:
            if t in range(len(y[i])+1):
                print(order[int(y[i][t-1].name.split('_')[-1])-1].index(i+1)-1)
                problem+=y[i][t-1]+y[order[int(y[i][t-1].name.split('_')[-1])-1][order[int(y[i][t-1].name.split('_')[-1])-1].index(i+1)-1]-1][int(y[i][t-1].name.split('_')[-1])-1]<= 1

    for i in range(numberOfCustomers):
        problem+=pulp.lpSum(w[i][k] for k in range(len(w[i])) ) <= 1
        

        
    if problem.solve() == 1:
        return y, x

def operate_lists(inputY, inputX, order):
    for y in inputY:
        if y[2] == 1:
            for x in inputX:
                if x[0] == y[0] and x[3] == 1:
                    idx = next(i for i, o in enumerate(order) if o[0] == x[0])
                    order[idx].insert(order[idx].index(x[2]), x[1])

def decode_input_Y_objects(input_str_list):
    values_list = []
    for input_str in input_str_list:
        parts = str(input_str).split('_')
        try:
            values = [int(parts[1]), int(parts[2])]
        except ValueError:
            continue
        values.append(input_str.varValue)
        values_list.append(values)
    return values_list

def decode_input_X_objects(input_str_list):
    values_list = []
    for input_str in input_str_list:
        parts = str(input_str).split('_')
        try:
            values = [int(parts[1]), int(parts[2]), int(parts[3])]
        except ValueError:
            continue
        values.append(input_str.varValue)
        values_list.append(values)
    return values_list

def extract_nested(nested_list):
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(extract_nested(item))
        else:
            result.append(item)
    return result


SS = IIP()
print(SS)

decodedSSY = decode_input_Y_objects(extract_nested(SS[0]))
decodedSSX = decode_input_X_objects(extract_nested(SS[1]))

print(decodedSSX)
print(decodedSSY)






 
