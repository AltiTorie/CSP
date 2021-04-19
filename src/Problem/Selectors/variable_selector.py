from abc import ABC, abstractmethod

from src.Problem.problem import Problem


class VariableSelector(ABC):
    def __init__(self, problem):
        self.problem = problem

    @abstractmethod
    def select(self, assignment, custom_domains=None):
        ...


class TakeFirstVariableSelector(VariableSelector):
    def select(self, assignment, custom_domains=None):
        unassigned_variables = [variable for variable in self.problem.variables if variable not in assignment]
        if unassigned_variables:
            return unassigned_variables[0]


class MinimumRemainingVariableSelector(VariableSelector):
    def select(self, assignment, custom_domains=None):
        domains = custom_domains if custom_domains else self.problem.domains
        unassigned_variables = [variable for variable in self.problem.variables if variable not in assignment]
        if unassigned_variables:
            return min(unassigned_variables, key=lambda var: len(domains[var]))


class DegreeVariableSelector(VariableSelector):
    def select(self, assignment, custom_domains=None):
        unassigned_variables = [variable for variable in self.problem.variables if variable not in assignment]
        if unassigned_variables:
            return max(unassigned_variables, key=lambda var: len(self.problem.constraints[var]))
