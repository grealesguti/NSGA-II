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

#rf=os.listdir('geant4sim/SingLYSO/NSGAII/PyNSGA/NSGA-II/ROOT/')
test='Test_Cont_071222v2'
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
for i in idx_sort:
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
    allobj1.append(obj1)  
    allobj2.append(obj2)
    
ims=[]
fig, ax = plt.subplots()
plt.grid()
plt.xlim([-20000, -2000])
plt.ylim([200, 900])
# specifying horizontal line type
plt.axhline(y = 3*3*28.5*2, color = 'k', linestyle = '--')
plt.axhline(y = 2.4*3*28.5*2, color = 'k', linestyle = '--')
plt.axhline(y = 3.75*3*28.5*2, color = 'k', linestyle = '--')
for i in range(rf_len):
	im=plt.scatter(allobj1[i],allobj2[i])
	plt.xlabel('Light Collection [-ph]')
	plt.ylabel('Volume [mm³]')
	plt.savefig('pictures/ROOT/'+test+'/'+'Generation_'+str(i)+'.png')
	ims.append([im])
	
	
	
	
	
