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

class G4Job:
        def __init__(self,CurrentFolder="/storage/af/user/greales/simG4/BTL_LYSOARRAY_LO_G4/",OutFolder="/storage/af/user/greales/simG4/outputs/", SubName="SubDefaultName", OutName="Out_NSGA", JobName="JobActionGC1FLResinMuon.sh", Generation=1, indv=1):
                self.CurrentFolder = CurrentFolder
                self.OutFolder = OutFolder
                self.SubName = SubName
                self.OutName = OutName
                self.JobName = JobName
                self.Generation = Generation
                self.indv = indv

        def CleanOut(self):
            p = subprocess.call(['condor_rm',"greales"])
            p = subprocess.call(['rm',"SubFiles/"+self.SubName+"*"])
            p = subprocess.call(['rm',self.OutFolder+self.OutName+"*"])
            return 0

        def SubWrite(self , Children=[]):
            nvar=len(Children[0].features)
            nvar+=-1
            f = open("SubFiles/"+self.SubName+".sub", "a")
            f.write("Universe = vanilla\n")
            f.write("executable = "+self.CurrentFolder+"JobFiles/"+self.JobName+"\n")
            if(Children==[]):
                #f.write('arguments ="-a Generation_'+str(self.Generation)+'_ -w $(indv) -v $(var)"\n')
                f.write('arguments ="-a Generation_'+str(self.Generation)+'_ -v $(var)"\n')
                f.write("Output  ="+self.OutFolder+self.OutName+str(self.Generation)+"_1.out"+"\n")
            else:
                f.write('arguments ="-a Generation_$(gen)_$(indv)"\n')
                f.write("Output  ="+self.OutFolder+self.OutName+"_$(gen)_$(indv)"+".out"+"\n")
            f.write("Error   = /storage/af/user/greales/simG4/errors/error_job$(Cluster).out\n")
            f.write("Log     = /storage/af/user/greales/simG4/logs/log_job$(Cluster).out\n")
            f.write("requirements = Machine =!= LastRemoteHost\n")
            f.write("WHEN_TO_TRANSFER_OUTPUT = ON_EXIT_OR_EVICT\n")
            f.write('+JobQueue = "Short"\n')
            f.write("+MaxRuntime = 7000\n")
            f.write("+RunAsOwner = True\n")
            f.write("+InteractiveUser = True\n")
            f.write("+SingularityBindCVMFS = True\n")
            f.write('+SingularityImage = "/cvmfs/singularity.opensciencegrid.org/cmssw/cms:rhel7"\n')
            f.write("x509userproxy = $ENV(X509_USER_PROXY)\n")
            f.write("RequestDisk = 2000000\n")
            f.write("RequestMemory = 2000\n")
            f.write("RequestCpus = 1\n")
            f.write("on_exit_remove = ((ExitBySignal == False) && (ExitCode == 0)) || (JobStatus=?=3)\n")
            f.write("on_exit_hold = (ExitBySignal == True) || (ExitCode != 0)\n")
            f.write("+PeriodicRemove = ((JobStatus =?= 2) && ((MemoryUsage =!= UNDEFINED && MemoryUsage > 2.5*RequestMemory)))\n")
            f.write("should_transfer_files = Yes\n")
            f.write("max_retries = 3\n")
            if(Children=[]):
                f.write("Queue 1\n")
            else:
                f.write("Queue var, indv, gen from (\n")
                for i in Children:
                    cmd="{"
                    #for var in i.features:
                    #    cmd=cmd+"-"+str(var)
                    cmd=cmd+str(i.features)+"-"+str(2-i.features)
                    f.write(cmd+"} , "+str(i.idx)+" , "+str(i.Generation)+" , "+str(nvar)+"\n")
                f.write(")\n")
            f.close()
            
            return 0

        def SubLaunch(self):
            p = subprocess.call(["condor_submit",self.CurrentFolder+"SubFiles/"+self.SubName+".sub"])
            return 0

        def SubMonitor(self, wait=2, maxwait=3600, ptime=60):
            tc=0
            Subname=self.OutFolder+self.OutName+str(self.Generation)
            print("Looking for:"Subname)
            if(self.CheckIndv(Subname))
                print("File Found.")
                subprocess.call(["date"])
                return 0
            else:
                print("Waiting")
                subprocess.call(["date"])
                while(tc<maxwait):
                    #print(".", end = "") 
                    print(".",end='')  
                    #print(tc/60)
                    #sys.stdout.write(". ")
                    if(self.CheckIndv(Subname)):
                        print("File Found.")
                        subprocess.call(["date"])
                        return 0
                    time.sleep(wait)
                    tc+=wait
                    if(tc>maxwait):
                        print("Time Limit")
                        subprocess.call(["date"])
                        return 1

        def CheckIndv(self, mainname):
            finished=0
            for cc in range(self.indv)
                name=mainname+"_"+str(cc)+".out"
                if(path.exists(name)):
                    finished+=1
            if finished == self.indv:
                return True
            else:
                return False


        def TierIIRun(self, population):
                    self.SubWrite(population)
                    self.SubLaunch()
                    self.SubMonitor()
    
