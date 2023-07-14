from nsga2.problem import Problem
from nsga2.evolution import Evolution
#import matplotlib.pyplot as plt
import math
import ROOT
from nsga2.G4Inp import G4Inp

G4input = G4Inp(CurrentFolder="/storage/af/user/greales/simG4/BTL_LYSOARRAY_LO_G4/", OutFolder =  "/storage/af/user/greales/simG4/outputs/", SubName="SubDefaultName", OutName="Out_NSGA", JobName="JobActionNSGATestGmsh.sh", SiPMS=False, LYSOL=True, ROOTName='Generation_', RelativeFolder="../../../Results/", Singularity = '+SingularityImage="/storage/af/user/greales/SingDir/sandG4Gmsh"',SZloc=False)
'''
def f1(indv, generation, PopName=G4input.ROOTName,Pop=0,Folder=G4input.RelativeFolder):

    f=PopName+str(generation)+"_"+str(indv)+"_0.root"
    ff = Folder+file_path;
    try:
    	with  ROOT . TFile . Open ( Folder+f ," READ ") as inFile:
            tree = inFile . Get ("EndOfRun")
            tree.GetEntry(0)
            LC = getattr(tree,"fLCAvg")
    #inFile.Close()
            return -1*LC
    except Exception as e:
        print(f"\nError reading LC from file {ff}: {e}")
        return 0



def f2(indv, generation, PopName=G4input.ROOTName,Pop=0,Folder=G4input.RelativeFolder):
    f=PopName+str(generation)+"_"+str(indv)+"_0.root"
    ff = Folder+file_path;
    try:
    	with  ROOT . TFile . Open ( Folder+f ," READ ") as inFile:
            tree = inFile . ndv, generation, PopName=G4input.ROOTName,Pop=0,Folder=G4input.RelativeFolder):
    f=PopName+str(generation)+"_"+str(indv)+"_0.root"
    inFile = ROOT . TFile . Open ( Folder+f ," READ ")
    tree = inFile . Get ("EndOfRun")
    tree.GetEntry(0)
    LC = getattr(tree,"fLCAvg")
    inFile.Close()
    return -1*LC
'''

def f1(indv, generation, PopName=G4input.ROOTName,Pop=0,Folder=G4input.RelativeFolder):
    f=PopName+str(generation)+"_"+str(indv)+"_0.root"
    try:    
        inFile = ROOT . TFile . Open ( Folder+f ," READ ")
        tree = inFile . Get ("EndOfRun")
        tree.GetEntry(0)
        LC = getattr(tree,"fLCAvg")
        inFile.Close()
    except Exception as e:
        print("Exception in LC gen. ",str(generation)," indv. ",str(indv))
        LC = -1e9
    return -1*LC

def f2(indv, generation, PopName=G4input.ROOTName,Pop=0,Folder=G4input.RelativeFolder):
    f=PopName+str(generation)+"_"+str(indv)+"_0.root"
    try:
        inFile = ROOT . TFile . Open ( Folder+f ," READ ")
        tree = inFile . Get ("EndOfRun")
        tree.GetEntry(0)
        Vol = getattr(tree,"fVolume")
        inFile.Close()
    except Exception as e:
        print("Exception in Vol gen. ",str(generation)," indv. ",str(indv))
        Vol = 1e9
    return Vol

def f1v2(individual_id, generation_num, Population_name=G4input.ROOTName,Population = 0, ROOT_Folder=G4input.RelativeFolder, tree_name="EndOfRun", variable_name="fLCAvg",exception_return=0):
    file_path = Population_name+str(generation_num)+"_"+str(individual_id)+"_0.root"
    f = ROOT_Folder+file_path;
    try:
        with ROOT.TFile.Open(ROOT_Folder+file_path, "READ") as root_file:
            tree = root_file.Get(tree_name)
            if not tree:
                raise Exception(f"TTree '{tree_name}' not found in ROOT file {file_path}")
            tree.GetEntry(0)
            value = getattr(tree, variable_name)
            return -1 * value
    except Exception as e:
        print(f"\nError reading file {file_path}: {e}")
        return exception_return

def f2v2(individual_id, generation_num, Population_name=G4input.ROOTName,Population = 0, ROOT_Folder=G4input.RelativeFolder, tree_name="EndOfRun", variable_name="fVolume",exception_return=513):
    file_path = Population_name+str(generation_num)+"_"+str(individual_id)+"_0.root"
    try:
        with ROOT.TFile.Open(ROOT_Folder+file_path, "READ") as root_file:
            tree = root_file.Get(tree_name)
            if not tree:
                raise Exception(f"TTree '{tree_name}' not found in ROOT file {file_path}")
            tree.GetEntry(0)
            value = getattr(tree, variable_name)
            return -1 * value
    except Exception as e:
        print(f"\nError reading file {file_path}: {e}")

n_of_variables=5*2+1

var_range=[(18.5,28.5),(0.25,2.25),(0.25,2.25),(0.25,2.25),(0.25,2.25),(0.25,2.25),(0.25,2.25),(0.25,2.25),(0.25,2.25),(0.25,2.25),(0.25,2.25)]

problem = Problem(num_of_variables=n_of_variables, objectives=[f1,f2], variables_range=var_range, same_range=False, expand=False, obj_idx=True)
evo = Evolution(problem,G4InputClass=G4input, mutation_param=20, num_of_generations=400, num_of_individuals=100, TierII=1,init_evo='',Generation_evo=0 )

indv=[i for i in evo.evolve()]
func = [i.objectives for i in indv]
feat = [i.features for i in indv]

print(func)
print(feat)

