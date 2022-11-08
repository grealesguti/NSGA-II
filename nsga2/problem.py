from nsga2.individual import Individual
import random
import ROOT

class Problem:

    def __init__(self, objectives, num_of_variables, variables_range, expand=True, same_range=False, obj_idx=False):
        self.num_of_objectives = len(objectives)
        self.num_of_variables = num_of_variables
        self.objectives = objectives
        self.expand = expand
        self.variables_range = []
        self.obj_idx = obj_idx
        if same_range:
            for _ in range(num_of_variables):
                self.variables_range.append(variables_range[0])
        else:
            self.variables_range = variables_range

    def generate_individual(self,generation=0,idx=0):
        individual = Individual()
        individual.Generation=generation
        individual.idx=idx
        individual.features = [random.uniform(*x) for x in self.variables_range]
        return individual

    def calculate_objectives(self, individual):
        if self.expand:
            if self.obj_idx:
                individual.objectives = [f(*individual.idx, *individual.Generation) for f in self.objectives]
            else:
                individual.objectives = [f(*individual.features) for f in self.objectives]
        else:
            if self.obj_idx:
                individual.objectives = [f(individual.idx, individual.Generation) for f in self.objectives]
            else:
                individual.objectives = [f(individual.features) for f in self.objectives]
            
