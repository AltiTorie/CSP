from abc import ABC, abstractmethod


class Constraint(ABC):
    def __init__(self, variables):
        self.variables = variables

    @abstractmethod
    def satisfied(self, assignment):
        msg = "%s is an abstract class" % self.__class__.__name__
        raise NotImplementedError(msg)
