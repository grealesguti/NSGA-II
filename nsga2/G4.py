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
        def __init__(self,CurrentFolder="/storage/af/user/greales/simG4/BTL_LYSOARRAY_LO_G4/",OutFolder="/storage/af/user/greales/simG4/outputs/", SubName="SubDefaultName", OutName="Out_NSGA", JobName="JobActionNSGATest.sh", Generation=1, indv=0,SiPMS=False):
                self.CurrentFolder = CurrentFolder
                self.OutFolder = OutFolder
                self.SubName = SubName
                self.OutName = OutName
                self.JobName = JobName
                self.Generation = Generation
                self.indv = indv
                self.SiPMS = SiPMS

        def CleanOut(self):
            p = subprocess.call(['condor_rm',"greales"])
            frm=os.listdir('SubFiles')
            for i in frm:
                p = subprocess.call(['rm',"SubFiles/"+i])
            frm=os.listdir('JobFiles')
            for i in frm:
                p = subprocess.call(['rm',"JobFiles/"+i])
            frm0=os.listdir('../../../../outputs')
            for i in frm0:
                if (i.startswith(self.OutName)):
                    p = subprocess.call(['rm','../../../../outputs/'+i])
            return 0

        def SubWrite(self , Children=[]):
            nvar=len(Children[0].features)
            nvar+=-1
            f = open("SubFiles/"+self.SubName+"_"+str(self.Generation)+".sub", "a")
            f.write("Universe = vanilla\n")
            f.write("executable = "+self.CurrentFolder+"JobFiles/"+self.JobName+"\n")
            if(len(Children)>1):
                #f.write('arguments ="-a Generation_'+str(self.Generation)+'_ -w $(indv) -v $(var)"\n')
                f.write('arguments ="-a Generation_$(gen)_$(indv)_ -v $(var) -z $(nvar)"\n')
                f.write("Output  ="+self.OutFolder+self.OutName+"_$(gen)_$(indv)"+".out"+"\n")
               
# f.write("Output  ="+self.OutFolder+self.OutName+str(self.Generation)+"_1.out"+"\n")
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
            if(Children==[]):
                f.write("Queue 1\n")
            else:
                checkoutnames=[]
                f.write("Queue var, indv, gen, nvar from (\n")
                for i in Children:
                    cmd="{"
                    for var in i.features:
                        cmd=cmd+"-"+str(var)
                    #cmd=cmd+str(i.features[0])+"-"+str(2-i.features[0])
                    f.write(cmd+"}, "+str(i.idx)+", "+str(i.Generation)+", "+str(nvar)+"\n")
                    checkoutnames.append(self.OutFolder+self.OutName+"_"+str(i.Generation)+"_"+str(i.idx)+".out")
                    self.indv+=1
                f.write(")\n")
            f.close()
            
            return checkoutnames

        def SubLaunch(self):
            p = subprocess.call(["condor_submit","SubFiles/"+self.SubName+"_"+str(self.Generation)+".sub"])
            return 0

        def SubMonitor(self,outnames, wait=2, maxwait=3600, ptime=60):
            tc=0
            #Subname=self.OutFolder+self.OutName+str(self.Generation)
            print("Looking for: OutName list")
            if(self.CheckIndv(outnames)==True):
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
                    if(self.CheckIndv(outnames)):
                        print("File Found.")
                        subprocess.call(["date"])
                        return 0
                    time.sleep(wait)
                    tc+=wait
                    if(tc>maxwait):
                        print("Time Limit")
                        subprocess.call(["date"])
                        return 1

        def CheckIndv(self, outnames):
            finished=0
            for name in outnames:
                #name=mainname+"_"+str(cc)+".out"
                if(path.exists(name)):
                    finished+=1
            if finished == self.indv:
                return True
            else:
                return False


        def TierIIRun(self, population):
                    outnames=self.SubWrite(population)
                    self.SubLaunch()
                    self.SubMonitor(outnames)
    
