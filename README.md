# OptModels
Model building modules for optimization.

Code is easier to write than most other libraries, and overwhelmingly fast calculations are achieved. C ++ booster speeds up core computation


## Genetic Algorithm

In computer science and operations research, a genetic algorithm (GA) is a metaheuristic inspired by the process of natural selection that belongs to the larger class of evolutionary algorithms (EA). Genetic algorithms are commonly used to generate high-quality solutions to optimization and search problems by relying on biologically inspired operators such as mutation, crossover and selection.[1. https://en.wikipedia.org/wiki/Genetic_algorithm#CITEREFMitchell1996] 


### sample
we can try genetic algorithm with a few lines of code
```
>>> from src.ga.algorithms import NSGAI
>>> from src import dtlz3
>>> nsga = NSGAI(dtlz3, 3, 3, 0, 10, 4)
>>> pop = nsga.run(num_step=1000, samplesize=100)

```

## Usage
clone:

`git clone https://github.com/yushikmr/OptModels.git`

preparing:

you should create vertual enviroment and build c++ booster.

cd `OptModels`

`bash init.sh`
