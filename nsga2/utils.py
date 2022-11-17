from nsga2.population import Population
from nsga2.G4 import G4Job
from nsga2.G4Inp import G4Inp
import random
import ROOT

class NSGA2Utils:

    def __init__(self, problem,G4input=G4Inp(), num_of_individuals=100,
                 num_of_tour_particips=2, tournament_prob=0.9, crossover_param=2, mutation_param=5, TierII=0, init="", Generation=0):

        self.problem = problem
        self.G4input = G4input
        self.num_of_individuals = num_of_individuals
        self.num_of_tour_particips = num_of_tour_particips
        self.tournament_prob = tournament_prob
        self.crossover_param = crossover_param
        self.mutation_param = mutation_param
        self.TierII = TierII
        self.init = init
        self.Generation = Generation


    def create_initial_population(self):
        if(self.init==""):
            population = self.create_random_population()
        else:
	    #print("ROOT Population")
            population = self.create_root_population()
        return population

    def create_random_population(self):
        population = Population()
        for ci in range(self.num_of_individuals):
            individual = self.problem.generate_individual(generation=self.Generation,idx=ci)
            population.append(individual)
        feat = [child.features for child in population.population]
        if self.TierII==1:
            print("TierII Launch jobs")
            g4job = G4Job(self.G4input,Generation=self.Generation)
            g4job.CleanOut()
            g4job.TierIIRun(population.population)
        for indv in population.population:        
            self.problem.calculate_objectives(indv)
        return population

    def create_root_population(self):
        f = ROOT.TFile(self.init,"READ")
        tree_pop = f.Get("tPopulation")
        tree_obj = f.Get("tObjectives")
        nIndv = self.num_of_individuals
        nFeat = self.problem.num_of_variables
        nObj = self.problem.num_of_objectives

        feat = [iev.features for iev in tree_pop]
        idv_feat = [iev.ind for iev in tree_pop]
        obj = [iev.objectives for iev in tree_obj]
        idv_obj = [iev.ind for iev in tree_obj]
        i=0
        j=0
        for ci in range(nIndv):
                individual = Individual()
                individual.idx=ci
                individual.Generation=self.Generation
                #individual.features = [x for x in feat[i:i+nFeat]]
                arr=[]            
                for i in range(nFeat):
                    arr.append(feat[j*nFeat+i])
                individual.features=arr    
                arr=[]
                for i in range(nObj):
                    arr.append(obj[j*nObj+i])
                    #individual.objectives = obj[j*nIndv+i]
                individual.objectives=arr    
                i=i+nFeat
                j+=1
                pop.append(individual)
        f.Close()
        return pop

    def fast_nondominated_sort(self, population):
        population.fronts = [[]]
        for individual in population:
            individual.domination_count = 0
            individual.dominated_solutions = []
            for other_individual in population:
                if individual.dominates(other_individual):
                    individual.dominated_solutions.append(other_individual)
                elif other_individual.dominates(individual):
                    individual.domination_count += 1
            if individual.domination_count == 0:
                individual.rank = 0
                population.fronts[0].append(individual)
        i = 0
        while len(population.fronts[i]) > 0:
            temp = []
            for individual in population.fronts[i]:
                for other_individual in individual.dominated_solutions:
                    other_individual.domination_count -= 1
                    if other_individual.domination_count == 0:
                        other_individual.rank = i+1
                        temp.append(other_individual)
            i = i+1
            population.fronts.append(temp)

    def calculate_crowding_distance(self, front):
        if len(front) > 0:
            solutions_num = len(front)
            for individual in front:
                individual.crowding_distance = 0

            for m in range(len(front[0].objectives)):
                front.sort(key=lambda individual: individual.objectives[m])
                front[0].crowding_distance = 10**9
                front[solutions_num-1].crowding_distance = 10**9
                m_values = [individual.objectives[m] for individual in front]
                scale = max(m_values) - min(m_values)
                if scale == 0: scale = 1
                for i in range(1, solutions_num-1):
                    front[i].crowding_distance += (front[i+1].objectives[m] - front[i-1].objectives[m])/scale

    def crowding_operator(self, individual, other_individual):
        if (individual.rank < other_individual.rank) or \
            ((individual.rank == other_individual.rank) and (individual.crowding_distance > other_individual.crowding_distance)):
            return 1
        else:
            return -1

    def create_children(self, population):
        children = []
        cc=self.num_of_individuals+1
        while len(children) < len(population):
            parent1 = self.__tournament(population)
            parent2 = parent1
            while parent1 == parent2:
                parent2 = self.__tournament(population)
            child1, child2 = self.__crossover(parent1, parent2,ind=cc)
            cc+=2
            self.__mutate(child1)
            self.__mutate(child2)
            children.append(child1)
            children.append(child2)
        feat = [child.features for child in children]
        if self.TierII==1:
            print("TierII Launch jobs")
            g4job = G4Job(self.G4input,Generation=self.Generation)
            g4job.TierIIRun(children)
        for child in children:           
            self.problem.calculate_objectives(child)
        return children

    def __crossover(self, individual1, individual2,ind=0):
        child1 = self.problem.generate_individual(generation=self.Generation,idx=ind+1)
        child2 = self.problem.generate_individual(generation=self.Generation,idx=ind+2)
        num_of_features = len(child1.features)
        genes_indexes = range(num_of_features)
        for i in genes_indexes:
            beta = self.__get_beta()
            x1 = (individual1.features[i] + individual2.features[i])/2
            x2 = abs((individual1.features[i] - individual2.features[i])/2)
            child1.features[i] = x1 + beta*x2
            child2.features[i] = x1 - beta*x2
        return child1, child2

    def __get_beta(self):
        u = random.random()
        if u <= 0.5:
            return (2*u)**(1/(self.crossover_param+1))
        return (2*(1-u))**(-1/(self.crossover_param+1))

    def __mutate(self, child):
        num_of_features = len(child.features)
        for gene in range(num_of_features):
            u, delta = self.__get_delta()
            if u < 0.5:
                child.features[gene] += delta*(child.features[gene] - self.problem.variables_range[gene][0])
            else:
                child.features[gene] += delta*(self.problem.variables_range[gene][1] - child.features[gene])
            if child.features[gene] < self.problem.variables_range[gene][0]:
                child.features[gene] = self.problem.variables_range[gene][0]
            elif child.features[gene] > self.problem.variables_range[gene][1]:
                child.features[gene] = self.problem.variables_range[gene][1]

    def __get_delta(self):
        u = random.random()
        if u < 0.5:
            return u, (2*u)**(1/(self.mutation_param + 1)) - 1
        return u, 1 - (2*(1-u))**(1/(self.mutation_param + 1))

    def __tournament(self, population):
        participants = random.sample(population.population, self.num_of_tour_particips)
        best = None
        for participant in participants:
            if best is None or (self.crowding_operator(participant, best) == 1 and self.__choose_with_prob(self.tournament_prob)):
                best = participant

        return best

    def __choose_with_prob(self, prob):
        if random.random() <= prob:
            return True
        return False      



