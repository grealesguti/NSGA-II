from nsga2.problem import Problem
from nsga2.evolution import Evolution
import matplotlib.pyplot as plt
import math
import ROOT

def f1(indv, generation, PopName="Generation_",Pop=0,Folder="../../../Results/"):
    f=PopName+str(generation)+"_"+str(indv)+"_0.root"
    inFile = ROOT . TFile . Open ( Folder+f ," READ ")
    tree = inFile . Get ("EndOfRun")
    tree.GetEntry(0)
    LC = getattr(tree,"fLCAvg")
    inFile.Close()
    return -1*LC

nindv=100
problem = Problem(num_of_variables=1, objectives=[f1], variables_range=[(0.7,1.7)], same_range=True, expand=False, obj_idx=True)
evo = Evolution(problem, mutation_param=20, num_of_generations=100, num_of_individuals=100, TierII=1)

indv=[i for i in evo.evolve()]
func = [i.objectives for i in indv]
feat = [i.features for i in indv]

print(func)
print(feat)

