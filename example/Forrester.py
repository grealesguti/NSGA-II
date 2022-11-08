from nsga2.problem import Problem
from nsga2.evolution import Evolution
import matplotlib.pyplot as plt
import math
import numpy as np

# Solution f(x)=-6.02 at x1=(0.757) 
# https://www.sfu.ca/~ssurjano/forretal08.html
def f1(x):
    s = (6*x[0]-2)**2*np.sin(12*x[0]-4)
    return s

problem = Problem(num_of_variables=1, objectives=[f1], variables_range=[(0, 1)], same_range=True, expand=False)
evo = Evolution(problem, mutation_param=20, num_of_generations=100,num_of_individuals=100)
indv=[i for i in evo.evolve()]
func = [i.objectives for i in indv]
feat = [i.features for i in indv]

print(func)
print(feat)
