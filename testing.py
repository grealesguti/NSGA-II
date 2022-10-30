import ROOT
import numpy as np
import sys
from nsga2.problem import Problem
from nsga2.population import Population
from nsga2.individual import Individual
from nsga2.utils import NSGA2Utils
import matplotlib.pyplot as plt

def f1(x):
    s = 0
    for i in range(len(x)-1):
        s += -10*math.exp(-0.2*math.sqrt(x[i]**2 + x[i+1]**2))
    return s

def f2(x):
    s = 0
    for i in range(len(x)):
        s += abs(x[i])**0.8 + 5*math.sin(x[i]**3)
    return s

problem = Problem(num_of_variables=3, objectives=[f1, f2], variables_range=[(-5, 5)], same_range=True, expand=False)
num_of_generations=1000
num_of_individuals=100
num_of_tour_particips=2
tournament_prob=0.9
crossover_param=2
mutation_param=5
utils = NSGA2Utils(problem, num_of_individuals, num_of_tour_particips, tournament_prob, crossover_param, mutation_param)

def create_root_population(fname,nIndv,nFeat,nObj):
    f = ROOT.TFile(fname,"READ")
    tree_pop = f.Get("tPopulation")
    tree_obj = f.Get("tObjectives")
    feat = [iev.features for iev in tree_pop]
    idv_feat = [iev.ind for iev in tree_pop]
    obj = [iev.objectives for iev in tree_obj]
    idv_obj = [iev.ind for iev in tree_obj]
    pop = Population()
    i=0
    j=0
    for _ in range(nIndv):
            individual = Individual()
            #individual.features = [x for x in feat[i:i+nFeat]]
            arr=[]            
            for i in range(nFeat):
                arr.append(feat[j*nFeat+i])
            individual.features=arr            
            arr=[]
            for i in range(nObj):
                arr.append(obj[j*nObj+i])
                #individual.objectives = obj[j*nIndv+i]
            individual.objectives=arr    
            i=i+nFeat
            j+=1
            pop.append(individual)
    f.Close()
    return pop

def PlotPopulation(pop):
    Front = pop.population
    function1 = [i.objectives[0] for i in Front]
    function2 = [i.objectives[1] for i in Front]
    plt.xlabel('Function 1', fontsize=15)
    plt.ylabel('Function 2', fontsize=15)
    plt.scatter(function1, function2)
    plt.show()
    return 0

def Plotvariables(pop,var,obj):
    Front = pop.population
    function1 = [i.objectives[obj] for i in Front]
    function2 = [i.features[var] for i in Front]
    plt.xlabel('Variable', fontsize=15)
    plt.ylabel('Objective', fontsize=15)
    plt.scatter(function2, function1)
    plt.show()
    return 0

fname="ROOT/NSGAII_99.root"
p=create_root_population(fname,100,3,2)
#p2=utils.fast_nondominated_sort(p)
#PlotPopulation(p)





