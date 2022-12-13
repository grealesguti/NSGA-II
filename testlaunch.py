from nsga2.individual import Individual
from nsga2.population import Population
from nsga2.G4 import G4Job
from nsga2.G4Inp import G4Inp

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
G4InputClass = G4Inp(CurrentFolder="/storage/af/user/greales/simG4/BTL_LYSOARRAY_LO_G4/", OutFolder =  "/storage/af/user/greales/simG4/outputs/", 
SubName="SubDefaultName", OutName="Out_NSGA", JobName="JobActionNSGATestGmsh.sh", SiPMS=False, LYSOL=False, 
ROOTName='Generation_', RelativeFolder="../../../Results/", Singularity = '+SingularityImage="/storage/af/user/greales/SingDir/sandG4Gmsh"')	

utils = NSGA2Utils(problem,G4InputClass, num_of_individuals=5, num_of_tour_particips=2, tournament_prob=0.9, crossover_param=2, mutation_param=5, TierII=1)
lst=[]
for j in range(5):
	i=Individual()
	i.features=[0.5+0.2*j,0.1+j]
	i.idx=j+1
	i.Generation=j+2
	lst.append(i)
	
	
test=G4Job(Generation=5,G4input=G4InputClass)

#test.CleanOut()
outlst=test.SubWrite(lst)

