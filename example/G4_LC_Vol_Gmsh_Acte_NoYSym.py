from nsga2.problem import Problem
from nsga2.evolution import Evolution
#import matplotlib.pyplot as plt
import math
import ROOT
from nsga2.G4Inp import G4Inp

G4input = G4Inp(CurrentFolder="/storage/af/user/greales/simG4/BTL_LYSOARRAY_LO_G4/", OutFolder =  "/storage/af/user/greales/simG4/outputs/", SubName="SubDefaultName", OutName="Out_NSGA", JobName="JobActionNSGATestGmsh.sh", SiPMS=False, LYSOL=False, ROOTName='Generation_', RelativeFolder="../../../Results/", Singularity = '+SingularityImage="/storage/af/user/greales/SingDir/sandG4Gmsh"')


def f1(indv, generation, PopName=G4input.ROOTName,Pop=0,Folder=G4input.RelativeFolder):
    f=PopName+str(generation)+"_"+str(indv)+"_0.root"
    inFile = ROOT . TFile . Open ( Folder+f ," READ ")
    tree = inFile . Get ("EndOfRun")
    tree.GetEntry(0)
    LC = getattr(tree,"fLCAvg")
    inFile.Close()
    return -1*LC

def f2(indv, generation, PopName=G4input.ROOTName,Pop=0,Folder=G4input.RelativeFolder):
    f=PopName+str(generation)+"_"+str(indv)+"_0.root"
    inFile = ROOT . TFile . Open ( Folder+f ," READ ")
    tree = inFile . Get ("EndOfRun")
    tree.GetEntry(0)
    Vol = getattr(tree,"fVolume")
    inFile.Close()
    return Vol

n_of_variables=5*2

#var_range=[(18.5,28.5),(0.25,1.75),(0.25,2.25),(0.25,2.25),(0.25,2.25),(0.25,2.25),(0.25,2.25),(0.25,2.25),(0.25,2.25),(0.25,2.25),(0.25,2.25)]

problem = Problem(num_of_variables=n_of_variables, objectives=[f1,f2], variables_range=[(0.25,1.75)], same_range=True, expand=False, obj_idx=True)
evo = Evolution(problem,G4InputClass=G4input, mutation_param=20, num_of_generations=400, num_of_individuals=100, TierII=1,init='ROOT/save58.root')

indv=[i for i in evo.evolve()]
func = [i.objectives for i in indv]
feat = [i.features for i in indv]

print(func)
print(feat)

