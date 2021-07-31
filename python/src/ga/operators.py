import numpy as np
import random

def simulatedBinaryCrossover(ind1, ind2, eta, probabiliry=None):
    l = max(len(ind1), len(ind2))
    if not probabiliry:
        probabiliry = 1 / l
    
    def sbc(x1, x2, eta):
        u = random.random()
        if u < 0.5:
            beta = (2 * u) ** (1 / (eta + 1))
        else:
            beta = (1 / (2 * (1 - u))) ** (1 / (eta + 1))

        c1 = 0.5 * ( (1 + beta) * x1 + (1 - beta) * x2)
        c2 = 0.5 * ( (1 - beta) * x1 + (1 + beta) * x2)
        if random.random() < 0.5:    
            return c1, c2
        else:
            return c2, c1
    for i in range(l):
        x1 = ind1[i]
        x2 = ind2[i]
        if random.random() < probabiliry:
            ind1[i], ind2[i] = sbc(x1, x2, eta)
    return ind1, ind2

def polynomialMutation(ind, eta, low, up, probabiliry=None):
    def pm(x, eta, low, up):
        u = random.random()
        if u < 0.5:
            delta = (2 * u) ** (1 / (1 + eta)) - 1
            c = x + delta * (x - low)
        else:
            delta = (1 / (2 * (1 - u))) ** (1 / (eta + 1)) - 1
            c = x + delta * (up - x)
        return c
        
    l = len(ind)
    if not probabiliry:
        probabiliry = 1 / len(ind)
    for i in range(l):
        x = ind[i]
        if random.random() < probabiliry:
            ind[i] = pm(x, eta, low, up)
    return ind