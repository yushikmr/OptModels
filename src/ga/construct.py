from dataclasses import dataclass, field

@dataclass
class Indivdual:
    """個体.
    """
    chromosomes:list
    num_objects:int
    directions:tuple=field(default_factory=tuple)
    fitness:list=field(default_factory=list)
    rank:int=None
    niche_count:float=None
    def __post_init__(self):
        if type(self.chromosomes) != list:
            raise TypeError(f'chromosomes must be list but {type(self.chromosomes)}.')
        if type(self.fitness) != list:
            raise TypeError(f'fitness must be list but {type(self.fitness)}.')
        if type(self.directions) != tuple:
            raise TypeError(f'fitness must be tuple but {type(self.directions)}.')
        if len(self.directions) == 0:
            self.directions = (1,) * self.num_objects
        if len(self.directions) != self.num_objects:
            raise ValueError(f'the length of direction must be {self.num_objects}')
    
    def __len__(self):
        return len(self.chromosomes)
    def __getitem__(self, idx):
        return self.chromosomes[idx]

    def addRank(self, rank):
        """addと言いつつ新しいインスタンスを返す
        """
        return Indivdual(chromosomes=self.chromosomes, 
                         num_objects=self.num_objects, 
                         directions=self.directions,
                         fitness=self.fitness,
                         rank=rank)
    def allocationFitness(self, func):
        """allocation objects by evaluate function
        """
        return Indivdual(chromosomes=self.chromosomes, 
                         num_objects=self.num_objects, 
                         directions=self.directions,
                         fitness=func(self.chromosomes, self.num_objects),
                         rank=self.rank)
    def update_chromosomes(self, newchromosomes):
        return Indivdual(
                        chromosomes=newchromosomes, 
                        num_objects=self.num_objects, 
                        directions=self.directions,
                        fitness=self.fitness,
                        rank=self.rank
                        )
    def add_niche_count(self, niche_count):
        return Indivdual(
                chromosomes=self.chromosomes, 
                num_objects=self.num_objects, 
                directions=self.directions,
                fitness=self.fitness,
                rank=self.rank,
                niche_count=niche_count
        )

class Population(list):
    """個体を集めた母集団
    """
    def __init__(self, *v):
        super().__init__(v)
    def ranks(self):
        return [ind.rank for ind in self]
    def extract_rank(self, rank):
        return [ind for ind in self if ind.rank == rank]
    @property
    def object_list(self):
        return [list(ind.fitness) for ind in self]
    def __add__(self, other):
        newpopulation = list(self) + list(other)
        return Population(*newpopulation)
    def __getitem__(self, idx:int):
        if type(list(self)[idx]) == list:
            return Population(*(list(self)[idx]))
        else:
            return list(self)[idx]
            
