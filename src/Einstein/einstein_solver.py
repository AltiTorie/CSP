import logging

from einstein import define_problem, print_nice_result
from einstein_constraints import AllDifferentConstraint, SameHouseConstraint, InLeftHouseConstraint, \
    InRightHouseConstraint, NextHouseConstraint
from src.Problem.Selectors.value_selector import LeastConstrainingValueSelector, TakeOriginalValueSelector
from src.Problem.Selectors.variable_selector import MinimumRemainingVariableSelector, DegreeVariableSelector
from src.Problem.algorithm import ForwardChecking, Backtracking, AC3
from src.Problem.solver import CSPSolver

if __name__ == '__main__':
    einstein_problem = define_problem()
    logging.info(f"____________EINSTEIN____________")
    solver = CSPSolver(
        problem=einstein_problem,
        algorithm_type=AC3,
        variable_selector=DegreeVariableSelector,
        value_selector=LeastConstrainingValueSelector,
        use_ac3=False
    )
    result = solver.get_solution()
    print_nice_result(result)
