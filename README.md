# OptModels
Model building modules for optimization

## Genetic Algorithm

In computer science and operations research, a genetic algorithm (GA) is a metaheuristic inspired by the process of natural selection that belongs to the larger class of evolutionary algorithms (EA). Genetic algorithms are commonly used to generate high-quality solutions to optimization and search problems by relying on biologically inspired operators such as mutation, crossover and selection.[1. https://en.wikipedia.org/wiki/Genetic_algorithm#CITEREFMitchell1996] 


### sample
we can try genetic algorithm with a few lines of code
```notebooks/NSGA.ipynb
from ga import NSGA
from problems import dtlz3

nsga = NSGA(evalfunc=dtlz3, numVariables=10, numObjects=2, low=0, up=1, shigma=5)
result = nsga.run(num_step=100)
```

## Usage
install:

`git clone https://github.com/yushikmr/OptModels.git`

preparing:

cd `OptModels`

`bash init.sh`