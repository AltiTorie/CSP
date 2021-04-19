from src.Problem.constraint import Constraint


class AllDifferentConstraint(Constraint):
    def __init__(self, variables):
        super().__init__(variables)

    def satisfied(self, assignment):
        assigned_vals = [assignment[var] for var in self.variables if var in assignment]
        return len(assigned_vals) == len(set(assigned_vals))


class SameHouseConstraint(Constraint):
    def __init__(self, var, other):
        super().__init__([var, other])
        self.var = var
        self.other = other

    def satisfied(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return True

        return assignment[self.var] == assignment[self.other]


class NextHouseConstraint(Constraint):
    def __init__(self, var, other):
        super().__init__([var, other])
        self.var = var
        self.other = other

    def satisfied(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return True

        return assignment[self.var] in [assignment[self.other] - 1, assignment[self.other] + 1]


class InLeftHouseConstraint(Constraint):
    def __init__(self, var, other):
        super().__init__([var, other])
        self.var = var
        self.other = other

    def satisfied(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return True

        return assignment[self.var] == assignment[self.other] - 1


class InRightHouseConstraint(Constraint):
    def __init__(self, var, other):
        super().__init__([var, other])
        self.var = var
        self.other = other

    def satisfied(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return True

        return assignment[self.var] == assignment[self.other] + 1
