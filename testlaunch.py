from nsga2.individual import Individual
from nsga2.population import Population
from nsga2.G4 import G4Job
from nsga2.utils import NSGA2Utils
from nsga2.evolution import Evolution

from nsga2.problem import Problem
import os
import subprocess
import ROOT


def f1(indv, generation, PopName="Generation_",Pop=0,Folder="../../../Results/"):
    f=PopName+str(generation)+"_"+str(indv)+"_0.root"
    inFile = ROOT . TFile . Open ( Folder+f ," READ ")
    tree = inFile . Get ("EndOfRun")
    tree.GetEntry(0)
    LC = getattr(tree,"fLCAvg")
    inFile.Close()
    return -1*LC

problem = Problem(num_of_variables=1, objectives=[f1], variables_range=[(0.5, 1.5)], same_range=True, expand=False,obj_idx=True)

utils = NSGA2Utils(problem, num_of_individuals=5, num_of_tour_particips=2, tournament_prob=0.9, crossover_param=2, mutation_param=5, TierII=1)
lst=[]
for j in range(5):
	i=Individual()
	i.features=[0.5+0.2*j]
	i.idx=j+1
	i.Generation=j+2
	lst.append(i)
test=G4Job(Generation=5)

test.CleanOut()
outlst=test.SubWrite(lst)

