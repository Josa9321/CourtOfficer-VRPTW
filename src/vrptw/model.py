import pyomo.environ as pyo
import numpy as np

from . import Instance
from .utils import Solution

def solve_instance(instance: Instance):
    model = define_model(instance)
    opt = pyo.SolverFactory('cplex')
    opt.solve(model)
    solution = Solution(model)
    return solution

def define_model(instance: Instance):
    model = pyo.ConcreteModel()

    model.n = instance.n
    model.V = pyo.Set(initialize=instance.V)
    model.N = pyo.Set(initialize=instance.N)
    model.K = pyo.Set(initialize=instance.K)

    model.time_matrix = pyo.Param(model.V, model.V, initialize=instance.time_dict, domain=pyo.NonNegativeReals)
    model.time_point = pyo.Param(model.V, initialize=instance.time_point, domain=pyo.NonNegativeReals)
    model.a = pyo.Param(model.V, initialize=instance.time_window_a, domain=pyo.NonNegativeReals)
    model.b = pyo.Param(model.V, initialize=instance.time_window_b, domain=pyo.NonNegativeReals)

    model.x = pyo.Var(model.V, model.V, model.K, domain=pyo.Binary)
    model.T = pyo.Var(model.V, model.K, domain=pyo.NonNegativeReals)

    model.C2 = pyo.Constraint(model.N, rule = ruleC2)
    model.C3 = pyo.Constraint(model.K, rule = ruleC3)
    model.C4 = pyo.Constraint(model.N, model.K, rule = ruleC4)
    model.C5 = pyo.Constraint(model.K, rule = ruleC5)
    model.C6 = pyo.Constraint(model.V, model.V, model.K, rule = ruleC6)
    model.C7a = pyo.Constraint(model.V, model.K, rule = ruleC7a)
    model.C7b = pyo.Constraint(model.V, model.K, rule = ruleC7b)
    model.CnoLoops = pyo.Constraint(model.V, model.K, rule = ruleNoLoops)

    model.obj = pyo.Objective(
        expr=sum(
            model.time_matrix[i, j] * model.x[i, j, k]
            for i in model.V
            for j in model.V
            for k in model.K
        ),
        sense=pyo.minimize,
    )
    return model

def ruleC2(model, i):
    return sum(model.x[i, j, k] for j in model.V if j != i for k in model.K) == 1

def ruleC3(model, k):
    return sum(model.x[0, j, k] for j in model.V if j != 0) == 1

def ruleC4(model, j, k):
    return sum(model.x[i, j, k] for i in model.V if i != j) == sum(model.x[j, i, k] for i in model.V if i != j)

def ruleC5(model, k):
    return sum(model.x[i, model.n-1, k] for i in model.V if i != model.n-1) == 1

def ruleC6(model, i, j, k):
    if i == j:
        return pyo.Constraint.Skip
    else:
        return model.T[i, k] + model.time_point[i] + model.time_matrix[i, j] <= model.T[j, k] + (1 - model.x[i, j, k]
            ) * 1.01*max(0, model.b[i] + model.time_point[i] + model.time_matrix[i, j] - model.a[j])

def ruleC7a(model, i, k):
    return model.T[i, k] >= model.a[i]

def ruleC7b(model, i, k):
    return model.T[i, k] <= model.b[i]

def ruleNoLoops(model, i, k):
    return model.x[i, i, k] == 0
