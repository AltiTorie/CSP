import pickle
from abc import ABC, abstractmethod
from time import time
from typing import Dict
import numpy as np
from numba import jit

from src.Problem.Selectors.value_selector import ValueSelector, TakeOriginalValueSelector
from src.Problem.Selectors.variable_selector import VariableSelector, TakeFirstVariableSelector
from src.Problem.problem import Problem


class Algorithm(ABC):
    def __init__(self, problem: Problem, variable_selector: VariableSelector,
                 value_selector: ValueSelector):
        self.problem = problem
        self.variable_selector = variable_selector
        self.value_selector = value_selector
        self.visited_nodes = 0

    @abstractmethod
    def get_solution(self):
        msg = "%s is an abstract class" % self.__class__.__name__
        raise NotImplementedError(msg)

    @abstractmethod
    def get_solutions(self):
        msg = "%s is an abstract class" % self.__class__.__name__
        raise NotImplementedError(msg)


class Backtracking(Algorithm):
    def __init__(self, problem: Problem, variable_selector: VariableSelector,
                 value_selector: ValueSelector):
        super().__init__(problem, variable_selector, value_selector)

    def get_solution(self):
        self.visited_nodes = 0
        return self.__get_solution()

    def get_solutions(self):
        self.visited_nodes = 0
        return self.__get_solutions()

    def __get_solution(self, assignment: Dict = {}):  # noqa
        if len(assignment) == len(self.problem.variables):
            return assignment

        variable_to_assign = self.variable_selector.select(assignment)

        for value in self.value_selector.select_values_order(assignment, variable_to_assign):
            partial_assignment = assignment.copy()
            partial_assignment[variable_to_assign] = value
            self.visited_nodes += 1
            if self.problem.is_consistent(variable_to_assign, partial_assignment):
                result = self.__get_solution(partial_assignment)
                if result is not None:
                    return result
        return None

    def __get_solutions(self, assignment: Dict = {}):  # noqa
        all_solutions = []
        if len(assignment) == len(self.problem.variables):
            all_solutions.append(assignment)
            return all_solutions

        variable_to_assign = self.variable_selector.select(assignment)

        for value in self.value_selector.select_values_order(assignment, variable_to_assign):
            partial_assignment = assignment.copy()
            partial_assignment[variable_to_assign] = value
            self.visited_nodes += 1
            if self.problem.is_consistent(variable_to_assign, partial_assignment):
                result = self.__get_solutions(partial_assignment)
                if result:
                    all_solutions.extend(result)
        return all_solutions


class ForwardChecking(Algorithm):

    def __init__(self, problem: Problem, variable_selector: VariableSelector,
                 value_selector: ValueSelector):
        super().__init__(problem, variable_selector, value_selector)

    def get_solution(self):
        self.visited_nodes = 0
        return self.__get_solution(domains=self.problem.domains)

    def get_solutions(self):
        self.visited_nodes = 0
        return self.__get_soultions(domains=self.problem.domains)

    def __get_solution(self, assignment: Dict = {}, domains: Dict = {}):  # noqa
        if len(assignment) == len(self.problem.variables):
            return assignment

        selected_var = self.variable_selector.select(assignment, custom_domains=domains)

        for value in self.value_selector.select_values_order(assignment, selected_var, domains):
            new_assignment = assignment.copy()
            new_assignment[selected_var] = value

            self.visited_nodes += 1
            if self.problem.is_consistent(selected_var, new_assignment):
                new_domains = self.__clear_domains(new_assignment, selected_var, domains)

                result = self.__get_solution(new_assignment, new_domains)
                if result is not None:
                    return result
        return None

    def __get_soultions(self, assignment: Dict = None, domains: Dict = None):
        if not assignment:
            assignment = {}
        if not domains:
            domains = {}
        all_solutions = []
        if len(assignment) == len(self.problem.variables):
            all_solutions.append(assignment)
            return all_solutions

        selected_var = self.variable_selector.select(assignment, custom_domains=domains)

        for value in self.value_selector.select_values_order(assignment, selected_var, domains):
            new_assignment = assignment.copy()
            new_assignment[selected_var] = value

            self.visited_nodes += 1
            if self.problem.is_consistent(selected_var, new_assignment):
                cleared = self.__clear_domains(new_assignment, selected_var, domains)
                result = self.__get_soultions(new_assignment, cleared)
                if result:
                    all_solutions.extend(result)
        return all_solutions

    def __clear_domains(self, assignment, new_variable, domains):
        cleared_domains = pickle.loads(pickle.dumps(domains))

        for constraint in self.problem.constraints[new_variable]:
            for variable in constraint.variables:
                if variable not in assignment:
                    assignment[variable] = None
                    for value in domains[variable]:
                        if value in cleared_domains[variable]:
                            assignment[variable] = value
                            if not constraint.satisfied(assignment):
                                cleared_domains[variable].remove(value)
                    del assignment[variable]

        return cleared_domains


class AC3(Algorithm):
    def __init__(self, problem: Problem, variable_selector: VariableSelector = TakeFirstVariableSelector,
                 value_selector: ValueSelector = TakeOriginalValueSelector):
        super().__init__(problem, variable_selector, value_selector)

    def get_solution(self):
        self.visited_nodes = 0
        return self.__get_solution(domains=self.problem.domains)

    def get_solutions(self):
        self.visited_nodes = 0
        return self.__get_solutions(domains=self.problem.domains)

    def __get_solution(self, assignment=None, domains=None):
        if assignment is None:
            assignment = {}
        if domains is None:
            domains = {}
        if len(assignment) == len(self.problem.variables):
            return assignment

        selected_var = self.variable_selector.select(assignment, domains)

        for value in self.value_selector.select_values_order(assignment, selected_var, domains):
            new_assignment = assignment.copy()
            new_assignment[selected_var] = value
            self.visited_nodes += 1
            if self.problem.is_consistent(selected_var, new_assignment):
                domains_copy = pickle.loads(pickle.dumps(domains))
                domains_copy[selected_var] = [value]
                self.do_ac3(domains_copy)
                result = self.__get_solution(new_assignment, domains_copy)
                if result is not None:
                    return result
        return None

    def __get_solutions(self, assignment: Dict = {}, domains={}):  # noqa
        all_solutions = []
        if len(assignment) == len(self.problem.variables):
            all_solutions.append(assignment)
            return all_solutions

        selected_var = self.variable_selector.select(assignment, domains)

        for value in self.value_selector.select_values_order(assignment, selected_var, domains):
            new_assignment = assignment.copy()
            new_assignment[selected_var] = value
            self.visited_nodes += 1
            if self.problem.is_consistent(selected_var, new_assignment):
                domains_copy = pickle.loads(pickle.dumps(domains))
                domains_copy[selected_var] = [value]
                self.do_ac3(domains_copy)
                result = self.__get_solutions(new_assignment, domains_copy)
                if result:
                    all_solutions.extend(result)
        return all_solutions

    def do_ac3(self, domains):
        constraints_queue = [(vx, vy) for vx in self.problem.constraints
                             for constraint in self.problem.constraints[vx]
                             for vy in constraint.variables]
        while constraints_queue:
            x, y = constraints_queue.pop(0)
            removed = self.__remove_inconsistent_values(x, y, domains)
            if removed:
                new_constraints = [(vx, vy) for vx in self.problem.constraints
                                   for constraint in self.problem.constraints[vx]
                                   for vy in constraint.variables if vy == x]
                constraints_queue.extend(new_constraints)

    def __remove_inconsistent_values(self, x, y, domains):
        removed = False

        all_constraint = [constraint for constraint in self.problem.constraints[x] if y in constraint.variables]
        for x_value in domains[x]:
            satisfies = False
            for y_value in domains[y]:
                assignment = {x: x_value, y: y_value}
                if satisfies := all(constraint.satisfied(assignment) for constraint in all_constraint):
                    break
            if not satisfies:
                domains[x].remove(x_value)
                removed = True
        return removed
