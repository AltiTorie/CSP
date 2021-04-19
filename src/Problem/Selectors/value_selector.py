from abc import ABC, abstractmethod

from src.Problem.problem import Problem


class ValueSelector(ABC):
    def __init__(self, csp: Problem):
        self.csp = csp

    @abstractmethod
    def select_values_order(self, assignment, variable, domains=None):
        ...


class TakeOriginalValueSelector(ValueSelector):
    def select_values_order(self, assignment, variable, domains=None):
        if not domains:
            return self.csp.domains[variable]
        else:
            return domains[variable]


class LeastConstrainingValueSelector(ValueSelector):
    def select_values_order(self, assignment, variable, domains=None):
        if not domains:
            domains = self.csp.domains

        others_values_count = {}
        for value in domains[variable]:
            temp_assignment = assignment.copy()
            temp_assignment[variable] = value
            count = self.__get_count_of_possible_values(temp_assignment, variable, domains)
            others_values_count[value] = count

        return dict(sorted(others_values_count.items(), key=lambda item: item[1], reverse=True))

    def __get_count_of_possible_values(self, assignment, checked_variable, domains):
        counter = 0
        for constraint in self.csp.constraints[checked_variable]:
            for variable in constraint.variables:
                if variable not in assignment:
                    for value in domains[variable]:
                        temp_assignment = assignment.copy()
                        temp_assignment[variable] = value
                        if self.csp.is_consistent(variable, temp_assignment):
                            counter += 1
        return counter
