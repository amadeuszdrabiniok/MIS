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

numberOfCustomers = 120

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


# https://developers.google.com/optimization/routing/vrp