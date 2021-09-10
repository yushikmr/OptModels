
import random
from .operators import Operator
from .operators import NonDominatedSort

from .genetic_algorithms import Individual, Population, NSGA

class NSGAI(NSGA):
    """Non-Dminated Sorting Algorithm.
    """
    
    def __init__(
                self, 
                evalfunc, 
                numVariables:int, 
                numObjects:int, 
                low:float, 
                up:float, 
                shigma) -> None:
        """constructer 
        Args:
            evalfunc(function): evaluate function you want to optimize
            numVariables(int):the number of variables.
            numObjects: the number of objects.
            low(float): lower limit of variables.
            up(float): upper limit if variables.
            shigma(float): the parameter of niche count.
        """  

        super().__init__(1, numVariables, numObjects, low, up, shigma)
        self.generation = 1
        self.evalfunc = evalfunc

    def generate_init_population(self, samplesize:int)->Population:
        self.init_population = \
                Population([Individual([random.random() for i in range(self.numvariables)],
                                        self.numobjects) for j in range(samplesize)])

        return self.init_population


    def evaluate(self, population:Population) -> Population:
        """calculate fitness and allocate to individual
        should select evaluate function when NSGA object build.

        """
        objects = [self.evalfunc(ind.variables, self.numobjects) for ind in population.members]
        inds = [ind.allocate_objects(o) for ind, o in zip(population.members, objects)]
        fitted_population = Population(inds)
        return fitted_population
    

    def crossover(self, population:Population)->Population:
        """crossover by simulatedBinaryCrossover
        """
        members = population.members
        for i, couple in enumerate(zip(*[iter(members)]*2)):
            child1, child2 = Operator.simulatedBinaryCrossover(
                                                                couple[0].variables,
                                                                couple[1].variables, 
                                                                eta=10
                                                                )
            
            members[i] = couple[0].update_variables(child1)
            members[i+1] = couple[1].update_variables(child2)
        return Population(members)

    def mutation(self, population:Population)->Population:
        """mutation by polynomialMutation
        """
        members = population.members
        for i, ind in enumerate(members):
            child= Operator.polynomialMutation(ind.variables, eta=10, low=self.low, up=self.up)
            members[i] = ind.update_variables(child)
        return Population(members)
    
    def select(self, population:Population, num:int)->Population:
        """select next population by non-dominated-sort and sharing function
        
        """
        sortFunc = NonDominatedSort()
        selected_members = sortFunc(population).sorted().members[:num]
        return Population(selected_members)

    def evolution(self, population:Population)->Population:
        """crossover and mutation
        """
        cx_childlen = self.crossover(population)
        cxm_childlen = self.mutation(cx_childlen)
        return population + cxm_childlen

    
    def step(self, population:Population) -> Population:
        """the step of genetic algirithm. 
        Args:
         population(Population): sample 
        """
        num = len(population.members)
        population = self.evolution(population)
        # allocation fitness
        population = self.evaluate(population)
        # generational change
        population = self.select(population, num)
        self.generation += 1

        return population

    def run(self, num_step:int, init_population:Population=None, samplesize=100)->Population:
        """run evolutionary computation
        """
        if not init_population:
            population = self.generate_init_population(samplesize=samplesize)
        for i in range(num_step):
            population = self.step(population)
        return population




