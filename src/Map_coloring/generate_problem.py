from utils.graph_generator import generate_graph
from map_coloring_contraints import NotEqualConstraint
from src.Problem.problem import Problem
from utils.color import Color


def generate_problem(regions_num, plane_size):
    graph = generate_graph(regions_num, plane_size)

    variables = list(graph.neighbours.keys())
    domains = {}

    for variable in variables:
        domains[variable] = Color.get_list()

    problem = Problem(variables, domains)

    for region in graph.neighbours:
        for n in graph.neighbours[region]:
            problem.add_constraint(NotEqualConstraint(region, n))

    return problem, graph
