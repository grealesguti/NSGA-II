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

    def RootWrite(self,Gen=0):

        f = TFile('test_'+str(Gen)+'.root','recreate')
        t = TTree('tPopulation','tree with individual features')
        t2 = TTree('tObjectives','tree with individual features')
        maxn = 10
        n = array('i',[0])
        d = array('d',[0])
        t.Branch('ind',n,'ind/I')
        t.Branch('features',d,'features/D')
        t2.Branch('ind',n,'ind/I')
        t2.Branch('objectives',d,'objectives/D')
        c=0
        for i in self.population:
            n[0] = c
            for j in i.features:
                d[0]= float(j)
                #print("Indv: ",c," Feat: ", j)
                t.Fill()
            for j in i.objectives:
                d[0]= float(j)
                #print("Indv: ",c," Feat: ", j)
                t2.Fill()
            c+=1

        f.Write()
        f.Close()
