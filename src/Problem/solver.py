import logging
from time import time

from src.Problem.algorithm import AC3
from src.Problem.problem import Problem


def time_usage(func):
    def wrapper(*args, **kwargs):
        beg_ts = time()
        retval = func(*args, **kwargs)
        end_ts = time()
        logging.info(f"elapsed time for {func.__name__}: {(end_ts - beg_ts)}s")
        return retval

    return wrapper


class CSPSolver:
    def __init__(self,
                 problem: Problem,
                 algorithm_type,
                 variable_selector,
                 value_selector,
                 use_ac3
                 ):
        self.problem = problem

        self.use_ac3 = use_ac3
        self.select_variable_heuristic = variable_selector(self.problem)
        self.select_value_heuristic = value_selector(self.problem)
        self.algorithm = algorithm_type(self.problem,
                                        self.select_variable_heuristic,
                                        self.select_value_heuristic)

    @time_usage
    def get_solution(self):
        if self.use_ac3:
            ac3 = AC3(self.problem)
            ac3.do_ac3(self.problem.domains)
        solution = self.algorithm.get_solution()
        if solution:
            logging.info(f"Solution found, visited {self.algorithm.visited_nodes} nodes")
        else:
            logging.info(f"Solution not found! Visited {self.algorithm.visited_nodes} nodes")

        return solution

    @time_usage
    def get_solutions(self):
        if self.use_ac3:
            ac3 = AC3(self.problem)
            ac3.do_ac3(self.problem.domains)
        solutions = self.algorithm.get_solutions()
        logging.info(f"Found {len(solutions)} solutions, visited {self.algorithm.visited_nodes} nodes")
        return solutions
