
import random
import copy
from abc import ABC, abstractmethod
from .operators import Operator
from .operators import NonDominatedSort
from .construct import Indivdual, Population

class BaseAlgolithm(ABC):
    def __init__(self, evalfunc, numVariables:int, numObjects:int, low:float, up:float, shigma) -> None:  

        self.generation = 1
        self.numVariables = numVariables
        self.numObjects = numObjects
        self.evalfunc = evalfunc

        self.low = low
        self.up = up
        self.shigma = shigma

    def generate_init_population(self, samplesize:int)->Population:
        self.init_population = Population()
        for i in range(samplesize):
            self.init_population.append(
                        Indivdual(chromosomes=[random.random() for i in range(self.numVariables)],
                        num_objects=self.numObjects,
                        directions=(1,) * self.numObjects)
            )
        return self.init_population


    def evaluate(self, population:Population) -> Population:
        fitted_population = Population(*[p.allocationFitness(self.evalfunc) for p in population])
        return fitted_population
    
    def step(self, population:Population) -> Population:
        num = len(population)
        # evolution
        population = self.evolution(population)
        # allocation fitness
        population = self.evaluate(population)
        # generational change
        population = self.select(population, num)
        self.generation += 1

        return population

    @abstractmethod
    def evolution(self, population:Population) -> Population:
        return population

    @abstractmethod
    def select(self, population:Population) -> Population:
        return population
    
    def run(self, num_step:int, init_population:Population=None, samplesize=100)->Population:
        if not init_population:
            population = self.generate_init_population(samplesize=samplesize)
        for i in range(num_step):
            population = self.step(population)
        return population
  

class NSGA(BaseAlgolithm):

    def crossover(self, population:Population)->Population:
        childlen = copy.deepcopy(population)
        for i, couple in enumerate(zip(*[iter(childlen)]*2)):
            child1, child2 = Operator.simulatedBinaryCrossover(
                                                                couple[0].chromosomes,
                                                                couple[1].chromosomes, 
                                                                eta=10
                                                                )
            
            childlen[i] = couple[0].update_chromosomes(child1)
            childlen[i+1] = couple[1].update_chromosomes(child2)
        return childlen

    def mutation(self, population:Population)->Population:
        childlen = copy.deepcopy(population)
        for i, ind in enumerate(childlen):
            child= Operator.polynomialMutation(ind.chromosomes, eta=10, low=self.low, up=self.up)
            childlen[i] = ind.update_chromosomes(child)
        return childlen
    
    def select(self, population:Population, num:int)->Population:
        sortFunc = NonDominatedSort()
        sorted_population = sortFunc(population)
        next_population = Population()
        rank=1
        while len(next_population) < num:
            sub_population= [ind for ind in sorted_population if ind.rank == rank]
            if len(next_population) + len(sub_population) <= num:
                next_population.extend(sub_population)
            else:
                remainder = num - len(next_population)
                nc_s = [self.niche_count(ind, sub_population) for ind in sub_population]
                thred_nc = sorted(nc_s, reverse=True)[remainder]
                sub_populationNiche = [ind.add_niche_count(nc) for ind, nc in zip(sub_population, nc_s)]
                next_population.extend([ind for ind in sub_populationNiche if ind.niche_count >= thred_nc][:-1])
            rank+=1
        return next_population

    def evolution(self, population:Population)->Population:
        parent = copy.deepcopy(population)
        cx_childlen = self.crossover(parent)
        cxm_childlen = self.mutation(cx_childlen)
        return parent + cxm_childlen

    def sharingfunction(self, individual1, individual2)-> float:
        distance = sum([(i -j)**2 for i, j in zip(individual1, individual2)])**(0.5)
        if distance < self.shigma:
            return 1 - distance / self.shigma
        else:
            return 0
        
    def niche_count(self, ind:Indivdual, population:Population) -> float:
        nc = sum([self.sharingfunction(ind, ind2) for ind2 in population])
        return nc

