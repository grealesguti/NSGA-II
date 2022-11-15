from ROOT import TFile, TTree
from array import array

class Population:

    def __init__(self):
        self.population = []
        self.fronts = []

    def __len__(self):
        return len(self.population)

    def __iter__(self):
        return self.population.__iter__()

    def extend(self, new_individuals):
        self.population.extend(new_individuals)

    def append(self, new_individual):
        self.population.append(new_individual)

    def RootWrite(self,Gen=0,Folder='ROOT/',Name='NSGAII_'):

        f = TFile(Folder+Name+str(Gen)+'.root','recreate')
        t = TTree('tPopulation','tree with individual features')
        t2 = TTree('tObjectives','tree with individual objectives')
        t3 = TTree('tFronts','tree with individual ranks')
        maxn = 10
        n = array('i',[0])
        n1 = array('i',[0])
        d = array('d',[0])
        obj = array('d',[0])
        front = array('i',[0])
        t.Branch('ind',n,'ind/I')
        t.Branch('features',d,'features/D')
        t2.Branch('ind',n,'ind/I')
        t2.Branch('objectives',obj,'objectives/D')
        t3.Branch('ind',n1,'ind/I')
        t3.Branch('rank',front,'rank/I')
        c=0
        for i in self.population:
            n[0] = c
            for j in i.features:
                d[0]= float(j)
                #print("Indv: ",c," Feat: ", j)
                t.Fill()
            for j in i.objectives:
                obj[0]= float(j)
                #print("Indv: ",c," Feat: ", j)
                t2.Fill()
            c+=1
        for fts in self.fronts:
            r=0
            for i in fts:
                    n1[0]=i.idx
                    front[0]= r
                    t3.Fill()  
            r+=1

        f.Write()
        f.Close()
