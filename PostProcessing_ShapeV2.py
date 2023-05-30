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
import argparse
from ROOT import TFile, TTree
import matplotlib.pyplot as plt
from scipy.interpolate import splrep, splev,splprep
from scipy.interpolate import BSpline
import math
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="The name of the folder to be used.")
    parser.add_argument("generation",type=int, help="The number of the generation to plot.")
    parser.add_argument("--Ysym","-y", type=int, default=0, help="Y symmetry point.")
    parser.add_argument("--LYSOL","-l", type=int, default=0, help="Y symmetry point.")
    parser.add_argument("--save","-sv", type=int, default=1, help="Y symmetry point.")
    parser.add_argument("--Shape","-sh", type=int, default=0, help="Y symmetry point.")
    parser.add_argument("--ParetoFrontier","-pf", type=int, default=0, help="Y symmetry point.")
    parser.add_argument("--Filter","-f", type=int, default=0, help="Y symmetry point.")
    parser.add_argument("--LaunchIndv","-t", type=int, default=0, help="Y symmetry point.")

    return parser.parse_args()
def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{file_path} has been deleted.")
    else:
        print(f"{file_path} does not exist.")

def Plt_Crystal(xtop,ytop,xbot,ybot,pictures_folder,sv):
	
		ax = plt.gca()
		plot_line_from_points(xtop,ytop)
		plot_line_from_points(xbot,ybot)
		plt.plot([xbot[0], xbot[0]],[ybot[0],ytop[0]], color='blue')
		plt.plot([xbot[-1], xbot[-1]],[ybot[-1],ytop[-1]], color='blue')
		ax.set_ylim([-4, +4])

def SplinePts_NoYSym(num_vars,vars_tuple,Zhalf,Yhalf,indv):
	xtop=[]
	ytop=[]
	xbot=[]
	ybot=[]	
	Znode = int(num_vars/2)-1
	### top spline points
	for i in range(Znode+1):
			xtop.append(-Zhalf+Zhalf/Znode*i)
			ytop.append(vars_tuple[indv][i]*Yhalf)
	for i in range(Znode):
			xtop.append(-Zhalf+Zhalf/Znode*(i+Znode+1))
			ytop.append(ytop[Znode-i-1])
		
	### bottop spline points	
	for i in range(Znode+1):
			xbot.append(-Zhalf+Zhalf/Znode*i)
			ybot.append(-vars_tuple[indv][i+Znode+1]*Yhalf)
	for i in range(Znode):
			xbot.append(-Zhalf+Zhalf/Znode*(i+Znode+1))
			ybot.append(ybot[Znode-i-1])
	
	return xtop,ytop,xbot,ybot
	
def SplinePts_NoYSym_L(num_vars,vars_tuple,Yhalf,indv):
	xtop=[]
	ytop=[]
	xbot=[]
	ybot=[]	
	Znode = int(num_vars/2)-1
	### top spline points
	vars_tuplei=vars_tuple[indv]
	Zhalf=vars_tuplei[0]
	vars_tuplei=vars_tuplei[1:len(vars_tuplei)+1]
	for i in range(Znode+1):
			xtop.append(-Zhalf+Zhalf/Znode*i)
			ytop.append(vars_tuplei[i]*Yhalf)
	for i in range(Znode):
			xtop.append(-Zhalf+Zhalf/Znode*(i+Znode+1))
			ytop.append(ytop[Znode-i-1])
		
	### bottop spline points	
	for i in range(Znode+1):
			xbot.append(-Zhalf+Zhalf/Znode*i)
			ybot.append(-vars_tuplei[i+Znode+1]*Yhalf)
	for i in range(Znode):
			xbot.append(-Zhalf+Zhalf/Znode*(i+Znode+1))
			ybot.append(ybot[Znode-i-1])
	
	return xtop,ytop,xbot,ybot

def SplinePts_YSym_L(num_vars,vars_tuple,Yhalf,indv):
	xtop=[]
	ytop=[]
	xbot=[]
	ybot=[]	
	Znode = int(num_vars)-1
	### top spline points
	vars_tuplei=vars_tuple[indv]
	Zhalf=vars_tuplei[0]
	vars_tuplei=vars_tuplei[1:len(vars_tuplei)+1]
	print(" tuple indv: ",vars_tuplei)
	for i in range(Znode+1):
			xtop.append(-Zhalf+Zhalf/Znode*i)
			ytop.append(vars_tuplei[i]*Yhalf)
	for i in range(Znode):
			xtop.append(-Zhalf+Zhalf/Znode*(i+Znode+1))
			ytop.append(ytop[Znode-i-1])
	
	xbot=xtop
	ybot = [-i for i in ytop]
	### bottop spline points	

	
	return xtop,ytop,xbot,ybot
	
def SplinePts_YSym(num_vars,vars_tuple,Yhalf,Zhalf,indv):
	xtop=[]
	ytop=[]
	xbot=[]
	ybot=[]	
	Znode = int(num_vars)-1
	### top spline points
	vars_tuplei=vars_tuple[indv]
	Zhalf=vars_tuplei[0]
	vars_tuplei=vars_tuplei[0:len(vars_tuplei)+1]
	for i in range(Znode+1):
			xtop.append(-Zhalf+Zhalf/Znode*i)
			ytop.append(vars_tuplei[i]*Yhalf)
	for i in range(Znode):
			xtop.append(-Zhalf+Zhalf/Znode*(i+Znode+1))
			ytop.append(ytop[Znode-i-1])
	
	xbot=xtop
	ybot = [-i for i in ytop]
	### bottop spline points	

	
	return xtop,ytop,xbot,ybot

def plot_line_from_points(x_points, y_points):
	if len(x_points) != len(y_points):
		raise ValueError("x_points and y_points must have the same length")
	if len(x_points) != len(set(x_points)):
		raise ValueError("x_points must have unique values")
	if min(x_points) >= max(x_points) or min(y_points) >= max(y_points):
		raise ValueError("xmin must be less than xmax, and ymin must be less than ymax")

	tck = splrep( x_points, y_points,s=0)
	x_new = np.linspace(min(x_points), max(x_points), num=100)
	y_new = splev(x_new, tck)
	plt.scatter(x_points, y_points,color='blue')
	plt.plot(x_new, y_new,color='blue')
	#plt.show()

def get_files_in_folder(folder_name):
    return [file for file in os.listdir(folder_name) if os.path.isfile(os.path.join(folder_name, file))]

def get_branch_values(file_path, tree_name, branch_name):
    root_file = TFile(file_path)
    tree = root_file.Get(tree_name)
    branch = tree.GetBranch(branch_name)
    values = []
    for i in range(branch.GetEntries()):
        branch.GetEntry(i)
        values.append(branch.GetLeaf(branch_name).GetValue())
    root_file.Close()
    return values

def GetRootVariables(gen_file):
	### get all root results for gen
	ind_obj=get_branch_values(gen_file, "tObjectives", "ind")
	val_obj=get_branch_values(gen_file, "tObjectives", "objectives")
	ind_vars=get_branch_values(gen_file, "tPopulation", "ind")
	val_vars=get_branch_values(gen_file, "tPopulation", "features")
	ind_front=get_branch_values(gen_file, "tFronts", "ind")
	val_front=get_branch_values(gen_file, "tFronts", "rank")

	### Number of variables
	num_vars = ind_vars.count(1)	# number of design variables per individual
	num_indv = int(max(ind_vars))	# number of individuals
	min_indvidx=min(ind_vars)
	if(min_indvidx==0):
		num_indv+=1

	print("The number of vars per indv is :" + str(num_vars))
	print("The number indv is :" + str(num_indv))

	### get each individual objective for gen
	obj1=[val_obj[i] for i in range(len(val_obj)) if i % 2 == 0]	# LC
	obj2=[val_obj[i] for i in range(len(val_obj)) if i % 2 == 1]	# Vol

	### get each individual variables for gen
	ind_simpl = [i*num_vars for i in range(num_indv)]
	vars_tuple=[]
	for i in range(num_indv-1):
		lstvars=val_vars[ind_simpl[i]:ind_simpl[i+1]]
		vars_tuple.append(lstvars)
		
	return num_indv,num_vars,obj1,obj2,vars_tuple,lstvars

    
def find_strings_containing_substring(strings, substring):
    matching_strings = []
    for string in strings:
        if substring in string:
            matching_strings.append(string)
    return matching_strings

def get_multiple_index_elements(arr, num):
    return [arr[i] for i in range(len(arr)) if i % num == 0]
    
def create_folder(folder):
	if not os.path.exists(folder):  # Create required folders to store pictures
		os.makedirs(folder)
		print(f"{folder} created.")

	else:
		print(f"{folder} already exists.")	
		
def sort_strings_by_int(string_list):
    # Use the key parameter of the sort function to extract the integer from the string
    string_list.sort(key=lambda s: int(s.split('_')[-1].split('.')[0]))
    return string_list

def filter_values(x, y, y_range):
    # Create an empty list to store the filtered x and y values
	filtered_x = []
	filtered_y = []
    # Create an empty list to store the indexes of the filtered values
	filtered_indexes = []
	y0= min(y)
	y1=y0+y_range
	ymax=max(y)
    # Iterate through the x and y values
	while y0 < ymax:
		#print('test')
		for i in range(len(x)):
			if y0 <= y[i] <= y1:
				if not filtered_x or x[i] <= min(filtered_x):
						filtered_x.append(x[i])
						filtered_y.append(y[i])
						filtered_indexes.append(i)
		y0=y1
		y1=y0+y_range			
		
	return filtered_x, filtered_y, filtered_indexes
	
def closest_value(lst, value):
    closest = float('inf')
    closest_index = None
    for i, item in enumerate(lst):
        if abs(value - item) < abs(value - closest):
            closest = item
            closest_index = i
    return closest, closest_index

def SubLaunch(SubName,Generation):
            p = subprocess.call(["condor_submit","SubFiles/"+SubName+"_"+str(Generation)+".sub"])
            return 0
def SubWrite(features, ntimes, Vol,  ROOTName, Generation,SubName ='SubFileGen', JobName='JobName.sh', Singularity='Singularity', SiPMS=False, LYSOL=False):
            print("### Writting Sub File:")
            nvar=len(features)
            nvar+=-1
            f = open("SubFiles/"+SubName+"_"+str(Generation)+".sub", "w")
            f.write("Universe = vanilla\n")
            f.write("executable = ../../../JobFiles/"+JobName+"\n")
            if(len(features)>1):
                #f.write('arguments ="-a Generation_'+str(self.Generation)+'_ -w $(indv) -v $(var)"\n')
                f.write('arguments ="-a '+ROOTName+'$(gen)_$(Vol)_$(Item)_ -v $(var) -z $(nvar)')
                if(SiPMS):
                	f.write(' -t $(SiPM)')
                if(LYSOL):
                	f.write(' -l $(LYSOL)')	
                f.write('"\n')	
            
                f.write("Output  =Results/Out_$(gen)_$(vol)"+".out"+"\n")
               
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
            f.write(Singularity+"\n")
            f.write("x509userproxy = $ENV(X509_USER_PROXY)\n")
            f.write("RequestDisk = 2000000\n")
            f.write("RequestMemory = 2000\n")
            f.write("RequestCpus = 1\n")
            f.write("on_exit_remove = ((ExitBySignal == False) && (ExitCode == 0)) || (JobStatus=?=3)\n")
            f.write("on_exit_hold = (ExitBySignal == True) || (ExitCode != 0)\n")
            f.write("+PeriodicRemove = ((JobStatus =?= 2) && ((MemoryUsage =!= UNDEFINED && MemoryUsage > 2.5*RequestMemory)))\n")
            f.write("should_transfer_files = Yes\n")
            f.write("max_retries = 3\n")
            if(features==[]):
                f.write("Queue 1\n")
            else:
                checkoutnames=[]
                f.write("Queue var, vol, gen, nvar")

                if(SiPMS):
                	f.write(', SiPM')
                if(LYSOL):
                	f.write(', LYSOL')
                f.write(' from (\n')	
                featinit=0
                if(LYSOL):
                	featinit=1
                cmd="{"
                
                for y in features[featinit:len(features)+1]:
                	cmd=cmd+"-"+str(y)
                cmd=cmd+"}, "+str(Vol)+", "+str(Generation)+", "+str(nvar)
                if (SiPMS):
                	cmd=cmd+', '+str(features[featinit]*100)
                if(LYSOL):
                	cmd=cmd+', '+str(features[0])
                cmd=cmd+'\n'
                
                for i in range(ntimes):
                	f.write(cmd)
                f.write(")\n")
            f.close()
            
            #return #checkoutnames

	############
	### MAIN ###
	############
def main():
	### Initializations
	print('Initializations')
	args = parse_args()		# Parse arguments
	gmsh.initialize()		
	root_folder=args.folder	
	gen=args.generation
	folder_path='ROOT/'+root_folder # add path to ROOT/
	rf=os.listdir(folder_path)		# get all files in the folder
	NSGA_filenames = find_strings_containing_substring(rf, 'NSGAII_') # Get all root files
	NSGA_filenames=sort_strings_by_int(NSGA_filenames)
	prefix = folder_path+'/'
	#NSGA_files= list(map(lambda x: prefix + x, NSGA_filenames))
	NSGA_files=[prefix+s for s in NSGA_filenames]
	#print(NSGA_files)
	gen_file=folder_path+'/'+find_strings_containing_substring(rf, str(gen))[0] # Get last generation file or given gen.
	pictures_folder='pictures/ROOT/'+root_folder+'/Shape/'
	pictures_folder_pareto='pictures/ROOT/'+root_folder+'/Pareto/'
	pictures_folder_filter='pictures/ROOT/'+root_folder+'/Filter/'
	
	create_folder(pictures_folder)  # Create required folders to store pictures
	create_folder(pictures_folder_pareto)  # Create required folders to store pictures
	create_folder(pictures_folder_filter)  # Create required folders to store pictures

	print('### Initializations END')
	################
	### GEOMETRY ###
	################
	
	if(args.Shape>0):
		print('### SHAPE')
		# Get required input for plotting the crystal shapes
		num_indv,num_vars,obj1,obj2,vars_tuple,lstvars = GetRootVariables(gen_file)
		
		Zhalf=28.5
		Yhalf=1.5
		for indv in range(num_indv-1):
			### optional variable arguments
			
			### get spline control points for different scenarions
			if(args.Ysym==1):
				print("NoYSym")
				if (args.LYSOL==1):
					print("LYSOL")
					print("Length:",vars_tuple)
					xtop,ytop,xbot,ybot = SplinePts_NoYSym_L(num_vars-1,vars_tuple,Yhalf,indv)
				else:
					xtop,ytop,xbot,ybot = SplinePts_NoYSym(num_vars,vars_tuple,Zhalf,Yhalf,indv)
				# else we have a symmetrical case in Y!!!
			else:
				print("YSym")
				if (args.LYSOL==1):
					print("LYSOL")
					print("Length:",vars_tuple)
					xtop,ytop,xbot,ybot = SplinePts_YSym_L(num_vars-1,vars_tuple,Yhalf,indv)
				else:
					xtop,ytop,xbot,ybot = SplinePts_YSym(num_vars,vars_tuple,Yhalf,Zhalf,indv)
				# else we have a symmetrical case in Y!!!
			
			### plot and save	
			fig, ax = plt.subplots()
			try:
				Plt_Crystal(xtop,ytop,xbot,ybot,pictures_folder,1)	
				if(args.save==1):
					imagename="LYSO_Vol_"+str(round(obj2[indv],1))+"_LC_"+str(round(abs(obj1[indv]),1))
					save_name=pictures_folder+imagename
					print(save_name)
					plt.savefig(save_name, format='png', dpi=300, bbox_inches='tight')
			except:
				imagename="LYSO_Vol_"+str(round(obj2[indv],1))+"_LC_"+str(round(abs(obj1[indv]),1))
				print("### ERROR: ",pictures_folder+imagename)

	###################
	### GENERATIONS ###
	###################
	if(args.ParetoFrontier>0):
		print('### Pareto Frontier')
		ims=[]
		fig1, ax1 = plt.subplots()
		plt.grid()
		#plt.xlim([-20000, -2000])
		#plt.ylim([200, 900])
		# specifying horizontal line type
		plt.axhline(y = 3*3*28.5*2, color = 'k', linestyle = '--')
		plt.axhline(y = 2.4*3*28.5*2, color = 'k', linestyle = '--')
		plt.axhline(y = 3.75*3*28.5*2, color = 'k', linestyle = '--')
		g=0
		for NSGA_file in NSGA_files:
			#try:
				print("Generation: ",g )
				# Get required input for plotting the crystal shapes
				num_indv,num_vars,obj1,obj2,vars_tuple,lstvars = GetRootVariables(NSGA_file)
				ax1.scatter(obj1,obj2)
				if(g==0):
					ax1.set_xlabel('Light Collection [-ph]')
					ax1.set_ylabel('Volume [mm³]')
					ax1.set_xlim([min(obj1)*1.5, max(obj1)*0.8])
					ax1.set_ylim([min(obj2)*0.5, max(obj2)*1.1])
					
				imagename="LYSO_Pareto_Gen_"+str(g)
				save_name=pictures_folder_pareto+imagename
				#plt.show()
				plt.savefig(save_name, format='png', dpi=300, bbox_inches='tight')
				g+=1
				#ims.append([im])
				"""
			except:
				imagename="LYSO_Pareto_Gen_"+str(g)
				g+=1
				print("### ERROR: ",pictures_folder_pareto+imagename)
				"""
	##############
	### FILTER ###
	##############
	if(args.Filter>0):
		print('### Filter')
		# Get required input for plotting the crystal shapes
		num_indv,num_vars,obj1,obj2,vars_tuple,lstvars = GetRootVariables(gen_file)
		obj1f,obj2f,idxf=filter_values(obj1,obj2,20)
		print(idxf)
		fig1, ax1 = plt.subplots()
		plt.grid()
		ax1.set_xlabel('Light Collection [-ph]')
		ax1.set_ylabel('Volume [mm³]')
		plt.axhline(y = 3*3*28.5*2, color = 'k', linestyle = '--')
		plt.axhline(y = 2.4*3*28.5*2, color = 'k', linestyle = '--')
		plt.axhline(y = 3.75*3*28.5*2, color = 'k', linestyle = '--')
		ax1.set_xlim([min(obj1f)*1.1, max(obj1f)*0.9])
		ax1.set_ylim([min(obj2f)*0.5, max(obj2f)*1.1])
		ax1.scatter(obj1f,obj2f)
		#plt.show()
		imagename="LYSO_Filter_Pareto_Gen_"+str(args.generation)
		save_name=pictures_folder_filter+imagename
		plt.savefig(save_name, format='png', dpi=300, bbox_inches='tight')
		
		Zhalf=28.5
		Yhalf=1.5
		for indv in idxf:
			### optional variable arguments
			
			### get spline control points for different scenarions
			if(args.Ysym==1):
				print("NoYSym")
				if (args.LYSOL==1):
					print("LYSOL")
					#print("Length:",vars_tuple)
					xtop,ytop,xbot,ybot = SplinePts_NoYSym_L(num_vars-1,vars_tuple,Yhalf,indv)
				else:
					xtop,ytop,xbot,ybot = SplinePts_NoYSym(num_vars,vars_tuple,Zhalf,Yhalf,indv)				
			else:
				print("YSym")
				if (args.LYSOL==1):
					print("LYSOL")
					#print("Length:",vars_tuple)
					xtop,ytop,xbot,ybot = SplinePts_YSym_L(num_vars-1,vars_tuple,Yhalf,indv)
				else:
					xtop,ytop,xbot,ybot = SplinePts_YSym(num_vars,vars_tuple,Yhalf,Zhalf,indv)
			
			### plot and save	
			fig, ax = plt.subplots()
			#try:
			print("vars: ",indv," ",vars_tuple[indv])
			print("n_vars: ",num_vars)
			print(xtop)
			print(ytop)
			print(xbot)
			print(ybot)
			Plt_Crystal(xtop,ytop,xbot,ybot,pictures_folder,1)	
			if(args.save==1):
					imagename="LYSO_Vol_"+str(round(obj2[indv],1))+"_LC_"+str(round(abs(obj1[indv]),1))
					save_name=pictures_folder_filter+imagename
					print(save_name)
					plt.savefig(save_name, format='png', dpi=300, bbox_inches='tight')
			"""except:
				imagename="LYSO_Vol_"+str(round(obj2[indv],1))+"_LC_"+str(round(abs(obj1[indv]),1))
				print("### ERROR: ",pictures_folder_filter+imagename)*/		"""
	###################
	### Launch Indv ###
	###################
	if(args.LaunchIndv>0):
		print('### Launch Indv')
		# Get required input for plotting the crystal shapes
		num_indv,num_vars,obj1,obj2,vars_tuple,lstvars = GetRootVariables(gen_file)
		obj1f,obj2f,idxf=filter_values(obj1,obj2,20)
		closest, closest_index=closest_value(obj2f,500)
		print(obj2f[closest_index-1],' ', obj1f[closest_index-1],' ',obj1f[closest_index-1]/obj2f[closest_index-1])
		print(closest,' ' ,closest_index,' ', obj1f[closest_index],' ',obj1f[closest_index]/obj2f[closest_index])
		print(obj2f[closest_index+1],' ', obj1f[closest_index+1],' ',obj1f[closest_index+1]/obj2f[closest_index+1])
		original_idx = idxf[closest_index]
		print(vars_tuple[original_idx])
		SubWrite(vars_tuple[original_idx], 50, math.ceil(obj2f[closest_index]), 'testrootname', gen)
		#SubLaunch(gen)
		
			
if __name__ == '__main__':
    print('main')
    main()
        
