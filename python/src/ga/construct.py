from dataclasses import dataclass, field

@dataclass
class Indivdual:
    chromosomes:list
    num_objects:int
    directions:tuple=field(default_factory=tuple)
    fitness:list=field(default_factory=list)
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

class Population(list):
    def __init__(self, *v):
        super().__init__(v)