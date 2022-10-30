from nsga2.problem import Problem
from nsga2.evolution import Evolution
import matplotlib.pyplot as plt
import math
import ROOT

def f1(indv, generation, PopName="Out_NSGA_Generation_",Pop=0,Folder="./Results/"):
    f=Folder+PopName+str(generation)+"_"+indv+".root"
    inFile = ROOT . TFile . Open ( Folder+f ," READ ")
    tree = inFile . Get ("EndOfRun")
    tree.GetEntry(0)
    LC = getattr(tree,"fLCAvg")
    inFile.Close()
    return -1*LC

nindv=100
problem = Problem(num_of_variables=2, objectives=[f1, f2], variables_range=[(0.5,1.5)], same_range=True, expand=False, obj_idx=True)
evo = Evolution(problem, mutation_param=20, num_of_generations=100, num_of_individuals=nindv)
func = [i.objectives for i in evo.evolve()]

function1 = [i[0] for i in func]
function2 = [i[1] for i in func]
plt.xlabel('Function 1', fontsize=15)
plt.ylabel('Function 2', fontsize=15)
plt.scatter(function1, function2)
plt.show()
