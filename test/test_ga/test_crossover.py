from src.ga.operators.crossover import simulatedBinaryCrossover

def test_sbx1():

    ind1 = [-1, -1, -1]
    ind2 = [1, 1, 1]
    eta=30

    ind1, ind2 = simulatedBinaryCrossover(ind1, ind2, eta)