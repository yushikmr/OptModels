
import copy
from .operators import Operator
from .operators import NonDominatedSort

class BaseAlgolithm:
    def __init__(self) -> None:    
        pass

    

class NSGA(BaseAlgolithm):
    
    def crossover(self, population):
        childlen = copy.deepcopy(population)
        for i, couple in enumerate(zip(*[iter(childlen)]*2)):
            child1, child2 = Operator.simulatedBinaryCrossover(
                                                                couple[0].chromosomes,
                                                                couple[1].chromosomes, 
                                                                eta=10
                                                                )
            
            childlen[i] = couple[0].update_chromosomes(child1)
            childlen[i+1] = couple[1].update_chromosomes(child2)

    def mutation(self, population):
        childlen = copy.deepcopy(population)
        for i, ind in enumerate(childlen):
            child= Operator.polynomialMutation(ind.chromosomes, eta=10, low=-10, up=10)
            childlen[i] = ind.update_chromosomes(child)
        return childlen
    
    def sort(self, population):
        sortFunc = NonDominatedSort()
        sorted_population = sortFunc(population)
        return sorted_population
