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

#rf=os.listdir('geant4sim/SingLYSO/NSGAII/PyNSGA/NSGA-II/ROOT/')
folderpath='ROOT'
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
