import gmsh
import sys
import os
from os.path import exists
import subprocess
import numpy as np
import time
import ROOT
from os import listdir
from os.path import isfile, join
import os.path
from os import path
import matplotlib.pyplot as plt
import matplotlib.animation as animation

gmsh.initialize()

###############################################
### PRINT LYSO SHAPE WITH GMSH SPLINES FUNCTION
###############################################
def printLYSO(Znode,Ztot,Xtot,ptsY,imagename,Vol,LC):
	factory = gmsh.model.geo
	ptsYF=[]
	#print("first")
	for i in range(Znode+1):
		#print(ptsY[i])
		ptsYF.append(ptsY[i])
	#print("second")
	for i in range(Znode):
		#print(ptsY[Znode-i-1])
		ptsYF.append(ptsY[Znode-i-1])

	dZ=Ztot/Znode;
	pp=[]
	pm=[]
	for i in range(Znode*2+1):
		factory.addPoint(-1*Ztot+dZ*i, +1*ptsYF[i]*1.5,-Xtot/2,0,1000 + i)
		factory.addPoint(-1*Ztot+dZ*i, -1*ptsYF[i]*1.5,-Xtot/2,0,2000 + i)
		pp.append(1000 + i)
		pm.append(2000 + i)

	splp=gmsh.model.geo.addSpline(pp);
	splm=gmsh.model.geo.addSpline(pm);
	l0 = gmsh.model.geo.addLine(pp[Znode*2], pm[Znode*2]);
	lm = gmsh.model.geo.addLine(pp[0], pm[0]);

	gmsh.model.geo.synchronize();

	# Finally, we can add some comments by creating a post-processing view
	# containing some strings:
	v = gmsh.view.add("comments")
	# Add a text string in window coordinates, 10 pixels from the left and 10 pixels
	# from the bottom:
	gmsh.view.addListDataString(v, [5, 150], ["Vol = "+str(round(Vol, 1))+"[mm3]" ],["Align", "Center"])
	gmsh.view.addListDataString(v, [5, 125], ["LC = "+str(round(LC, 1))+"[ph]"],["Align", "Center"])
	gmsh.fltk.initialize()
	gmsh.write(imagename+".png")
	gmsh.fltk.finalize()

###############################################
### Extract information from generation given
###############################################
test='Test_2911'
folderpath='ROOT/'+test
rf=os.listdir(folderpath)
rf_len=len(rf)
genf=[]
allobj1=[]
allobj2=[]
for f in rf:
    genf.append(int(f[7:-5]))
idx_sort=np.argsort(genf)


ind_obj=[]
obj_obj=[]
#for i in idx_sort:
genpop=-1 ### Generation to draw
i = idx_sort[genpop]
f=rf[i]
inFile = ROOT . TFile . Open ( folderpath+'/'+f ," READ ")
tree_obj = inFile . Get ("tObjectives")
ind_objf=[]
obj_objf=[]
for j in range(tree_obj.GetEntries()):
        tree_obj.GetEntry(j)
        ind_objf.append(tree_obj.ind)
        obj_objf.append(tree_obj.objectives)
obj1=[obj_objf[i] for i in range(len(obj_objf)) if i % 2 == 0]
obj2=[obj_objf[i] for i in range(len(obj_objf)) if i % 2 == 1]

# If the file is the last in the list pass the frontier filter and get the variables!!
# store front information in root file!!!
ind_vars=[]
obj_vars=[]
tree_vars = inFile . Get ("tPopulation")
for j in range(tree_vars.GetEntries()):
        tree_vars.GetEntry(j)
        ind_vars.append(tree_vars.ind)
        obj_vars.append(tree_vars.features)
num_vars = ind_vars.count(1)
num_indv = max(ind_vars)
min_indvidx=min(ind_vars)
if(min_indvidx==0):
	num_indv+=1
	
print("The number of vars per indv is :" + str(num_vars))
print("The number indv is :" + str(num_indv))

ind_simpl = [i*num_vars for i in range(num_indv)]
varstup=[]
for i in range(num_indv-1):
	lstvars=obj_vars[ind_simpl[i]:ind_simpl[i+1]]
	varstup.append(lstvars)
	
ind_front=[]
obj_front=[]
tree_front = inFile . Get ("tFronts")
for j in range(tree_vars.GetEntries()):
        tree_vars.GetEntry(j)
        ind_front.append(tree_front.ind)
        obj_front.append(tree_front.rank)


######################################
### Print each shape of the generation
######################################
Ztot =28.5
Xtot=1.5*2
folder="pictures/ROOT/"
#for i in range(num_indv-1):
for i in range(2):
	if(obj_front[i]==0):
		imagename="LYSOTEST_Vol_"+str(round(obj_objf[i*2+1],1))+"_LC_"+str(round(obj_objf[i*2+2],1))
		gmsh.model.add(imagename)
		printLYSO(num_vars-1,Ztot,Xtot,varstup[i],folder+test+"/test/"+imagename,obj_objf[i*2+1],obj_objf[i*2+2])

	


######################################
### Get front numbers in py??
######################################

# def fast_nondominated_sort( population):
        # fronts = [[]]
        # for individual in population:
            # domination_count = 0
            # dominated_solutions = []
            # for other_individual in population:
                # if individual.dominates(other_individual):
                    # individual.dominated_solutions.append(other_individual)
                # elif other_individual.dominates(individual):
                    # individual.domination_count += 1
            # if individual.domination_count == 0:
                # individual.rank = 0
                # population.fronts[0].append(individual)
        # i = 0
        # while len(population.fronts[i]) > 0:
            # temp = []
            # for individual in population.fronts[i]:
                # for other_individual in individual.dominated_solutions:
                    # other_individual.domination_count -= 1
                    # if other_individual.domination_count == 0:
                        # other_individual.rank = i+1
                        # temp.append(other_individual)
            # i = i+1
            # fronts.append(temp)

# def dominates(other_individual,population):
        # and_condition = True
        # or_condition = False
        # for first, second in zip(self.objectives, other_individual.objectives):
            # and_condition = and_condition and first <= second
            # or_condition = or_condition or first < second
        # return (and_condition and or_condition)
        
        
