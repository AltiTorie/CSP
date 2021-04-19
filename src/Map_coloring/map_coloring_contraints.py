from src.Problem.constraint import Constraint


class NotEqualConstraint(Constraint):
    def __init__(self, region, other_region):
        super().__init__([region, other_region])
        self.region = region
        self.other_region = other_region

    def satisfied(self, assignment):
        if self.region not in assignment or self.other_region not in assignment:
            return True
        return assignment[self.region] != assignment[self.other_region]
