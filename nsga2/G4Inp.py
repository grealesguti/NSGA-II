import sys
import os
from os.path import exists
import subprocess
import numpy as np
import time
from os import listdir
from os.path import isfile, join
import os.path
from os import path

class G4Inp:
        def __init__(self,CurrentFolder="/storage/af/user/greales/simG4/BTL_LYSOARRAY_LO_G4/",OutFolder="/storage/af/user/greales/simG4/outputs/", SubName="SubDefaultName", OutName="Out_NSGA", JobName="JobActionNSGATest.sh", SiPMS=False,LYSOL=False,ROOTName='Generation_', RelativeFolder="../../../Results/", Singularity='+SingularityImage="/cvmfs/singularity.opensciencegrid.org/cmssw/cms:rhel7"\n'):
                self.CurrentFolder = CurrentFolder
                self.OutFolder = OutFolder
                self.SubName = SubName
                self.OutName = OutName
                self.JobName = JobName
                self.SiPMS = SiPMS
                self.LYSOL = LYSOL
                self.ROOTName = ROOTName
                self.RelativeFolder=RelativeFolder
                self.Singularity=Singularity


    
