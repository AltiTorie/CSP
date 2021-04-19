import logging
import pickle

from generate_problem import generate_problem
from src.Problem.Selectors.value_selector import LeastConstrainingValueSelector
from src.Problem.Selectors.variable_selector import DegreeVariableSelector
from src.Problem.algorithm import AC3
from src.Problem.solver import CSPSolver
from utils.visualizer import visualize

REGIONS_NUM = 15
PLANE_SIZE = 50
logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    problem, graph = generate_problem(REGIONS_NUM, PLANE_SIZE)

    with open('some_graph.pickle', 'wb') as f:
        pickle.dump(graph, f)
    # with open('some_graph.pickle', 'rb') as f:
    #     graph = pickle.load(f)
    logging.info(f"____________MAP_COLORING____________")
    solver = CSPSolver(
        problem=problem,
        algorithm_type=AC3,
        variable_selector=DegreeVariableSelector,
        value_selector=LeastConstrainingValueSelector,
        use_ac3=True
    )

    solutions = solver.get_solutions()
    result = solutions[0]
    ordered = [result[region].value for region in graph.neighbours]
    graph.to_json(PLANE_SIZE, f"graphs/{PLANE_SIZE}x{PLANE_SIZE}_{REGIONS_NUM}reg_csp.json", ordered)
    visualize(f"graphs/{PLANE_SIZE}x{PLANE_SIZE}_{REGIONS_NUM}reg_csp.json")
