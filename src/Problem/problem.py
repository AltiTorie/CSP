from src.Problem.constraint import Constraint


class Problem:
    def __init__(self, variables, domains):
        self.variables = variables
        self.domains = domains
        self.constraints = {}

        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise AttributeError(f"Variable {variable} needs a non-empty domain")

    def add_constraint(self, constraint: Constraint):
        for variable in constraint.variables:
            if variable not in self.variables:
                raise ValueError(f"Could not find {variable} in a problem {self}")
            else:
                self.constraints[variable].append(constraint)

    def is_consistent(self, variable, assignment):
        return all(constraint.satisfied(assignment) for constraint in self.constraints[variable])
