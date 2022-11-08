from nsga2.problem import Problem
from nsga2.evolution import Evolution
import matplotlib.pyplot as plt
import math

# Solution f(x)=-1.0316 at x1=(3,3) & x2=(-2,2)
# https://www.sfu.ca/~ssurjano/camel6.html
def f1(x):
    s = (4-2.1*x[0]**2+x[0]**4/3)*x[0]**2+x[0]*x[1]+(4*x[1]**2-4)*x[1]**2
    return s

problem = Problem(num_of_variables=2, objectives=[f1], variables_range=[(-5, 5)], same_range=True, expand=False)
evo = Evolution(problem, mutation_param=20, num_of_generations=100,num_of_individuals=100)
func = [i.objectives for i in evo.evolve()]

function1 = [i[0] for i in func]
print(function1)
