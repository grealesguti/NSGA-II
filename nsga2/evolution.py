from nsga2.utils import NSGA2Utils
from nsga2.population import Population
from nsga2.G4Inp import G4Inp
import ROOT

class Evolution:

    def __init__(self, problem,G4input=G4Inp(),TierII=0, num_of_generations=1000, num_of_individuals=100, num_of_tour_particips=2, tournament_prob=0.9, crossover_param=2, mutation_param=5):
        self.TierII=TierII
        self.utils = NSGA2Utils(problem,G4input, num_of_individuals, num_of_tour_particips, tournament_prob, crossover_param, mutation_param,TierII=self.TierII)
        self.population = None
        self.num_of_generations = num_of_generations
        self.on_generation_finished = []
        self.num_of_individuals = num_of_individuals
        print("### Initialized Evolution.")

    def evolve(self):
		print("## Evolve")
        self.population = self.utils.create_initial_population()
        print("## Init Population")
        self.utils.fast_nondominated_sort(self.population)
        for front in self.population.fronts:
            self.utils.calculate_crowding_distance(front)

        self.population.RootWrite(Gen=0)
        self.utils.Generation=1
        print("Generation 1: Initial Children")
        children = self.utils.create_children(self.population)
        returned_population = None
        #self.population.RootWrite(Gen=1)
        for i in range(self.num_of_generations):
            print("### Generation: ",i+2)
            self.utils.Generation=i+2
            self.population.extend(children)
            self.utils.fast_nondominated_sort(self.population)
            self.population.RootWrite(Gen=i+1)
            new_population = Population()
            front_num = 0
            while len(new_population) + len(self.population.fronts[front_num]) <= self.num_of_individuals:
                self.utils.calculate_crowding_distance(self.population.fronts[front_num])
                new_population.extend(self.population.fronts[front_num])
                front_num += 1
            self.utils.calculate_crowding_distance(self.population.fronts[front_num])
            self.population.fronts[front_num].sort(key=lambda individual: individual.crowding_distance, reverse=True)
            new_population.extend(self.population.fronts[front_num][0:self.num_of_individuals-len(new_population)])
            returned_population = self.population
            self.population = new_population
            self.utils.fast_nondominated_sort(self.population)
            for front in self.population.fronts:
                self.utils.calculate_crowding_distance(front)
            children = self.utils.create_children(self.population)
        return returned_population.fronts[0]
