from functools import reduce
from operator import mul
from math import *

def dtlz1(individual:list, obj:int) -> list:
    g = 100 * (len(individual[obj-1:]) + sum((xi-0.5)**2 - cos(20*pi*(xi-0.5)) for xi in individual[obj-1:]))
    f = [0.5 * reduce(mul, individual[:obj-1], 1) * (1 + g)]
    f.extend(0.5 * reduce(mul, individual[:m], 1) * (1 - individual[m]) * (1 + g) for m in reversed(range(obj-1)))
    return f

def dtlz2(individual:list, obj:int) -> list:
    xc = individual[:obj-1]
    xm = individual[obj-1:]
    g = sum((xi-0.5)**2 for xi in xm)
    f = [(1.0+g) *  reduce(mul, (cos(0.5*xi*pi) for xi in xc), 1.0)]
    f.extend((1.0+g) * reduce(mul, (cos(0.5*xi*pi) for xi in xc[:m]), 1) * sin(0.5*xc[m]*pi) for m in range(obj-2, -1, -1))
    return f

def dtlz3(individual:list, obj:int) -> list: 
    xc = individual[:obj-1]
    xm = individual[obj-1:]
    g = 100 * (len(xm) + sum((xi-0.5)**2 - cos(20*pi*(xi-0.5)) for xi in xm))
    f = [(1.0+g) *  reduce(mul, (cos(0.5*xi*pi) for xi in xc), 1.0)]
    f.extend((1.0+g) * reduce(mul, (cos(0.5*xi*pi) for xi in xc[:m]), 1) * sin(0.5*xc[m]*pi) for m in range(obj-2, -1, -1))
    return f
