import logging
from einstein_constraints import AllDifferentConstraint, SameHouseConstraint, InLeftHouseConstraint, InRightHouseConstraint, \
    NextHouseConstraint
from src.Problem.Selectors.value_selector import LeastConstrainingValueSelector, TakeOriginalValueSelector
from src.Problem.Selectors.variable_selector import MinimumRemainingVariableSelector, DegreeVariableSelector
from src.Problem.algorithm import ForwardChecking, Backtracking, AC3
from src.Problem.solver import CSPSolver
from src.Problem.problem import Problem

logging.basicConfig(level=logging.DEBUG)

NATIONALITIES = ["Englishman", "Swede", "Dane", "German", "Norwegian"]
COLORS = ["red", "white", "green", "yellow", "blue"]
DRINKS = ["tea", "coffee", "beer", "water", "milk"]
SMOKES = ["no filter", "cigars", "lights", "menthol", "pipe"]
PETS = ["dogs", "birds", "cats", "horses", "fish"]


def define_problem():
    # 1. The Norwegian lives in the first house.
    # 2. The Englishman lives in a red house.
    # 3. The Green house is directly on the left of the White house.
    # 4. The Dane drinks tea.
    # 5. The man who smokes lights lives next to the one who keeps cats.
    # 6. The owner of the Yellow house smokes Cigar.
    # 7. The German smokes Pipe.
    # 8. The man living in the centre house drinks milk.
    # 9. The man who smokes lights has a neighbour who drinks water.
    # 10. The person who smokes No filter has birds.
    # 11. The Swede keeps dogs as pets.
    # 12. The Norwegian lives next to the Blue house
    # 13. The man who keeps horses lives next to the Yellow house.
    # 14. The man who smokes Menthols drinks beer.
    # 15. The owner of the Green house drinks coffee.

    # Who owns fish?

    variables = []
    domains = {}

    for nationality in NATIONALITIES:
        variables.append(nationality)
        # 1. The Norwegian lives in the first house.
        if nationality == 'Norwegian':
            domains[nationality] = [0]
        else:
            domains[nationality] = list(range(5))

    for color in COLORS:
        variables.append(color)
        domains[color] = list(range(5))

    for drink in DRINKS:
        variables.append(drink)
        # 8. The man living in the centre house drinks milk.
        if drink == 'milk':
            domains[drink] = [2]
        else:
            domains[drink] = list(range(5))

    for smoke in SMOKES:
        variables.append(smoke)
        domains[smoke] = list(range(5))

    for pet in PETS:
        variables.append(pet)
        domains[pet] = list(range(5))

    problem = Problem(variables, domains)

    problem.add_constraint(AllDifferentConstraint(COLORS))
    problem.add_constraint(AllDifferentConstraint(NATIONALITIES))
    problem.add_constraint(AllDifferentConstraint(DRINKS))
    problem.add_constraint(AllDifferentConstraint(SMOKES))
    problem.add_constraint(AllDifferentConstraint(PETS))

    # 1. Already taken care of.

    # 2. The Englishman lives in a red house.
    problem.add_constraint(SameHouseConstraint("red", "Englishman"))

    # 3. The Green house is directly on the left of the White house.
    problem.add_constraint(InLeftHouseConstraint("green", "white"))
    problem.add_constraint(InRightHouseConstraint("white", "green"))

    # 4. The Dane drinks tea.
    problem.add_constraint(SameHouseConstraint("Dane", "tea"))

    # 5. The man who smokes lights lives next to the one who keeps cats.
    problem.add_constraint(NextHouseConstraint("lights", "cats"))
    # problem.add_constraint(NextToConstraint("cats", "lights"))

    # 6. The owner of the Yellow house smokes cigars.
    problem.add_constraint(SameHouseConstraint("yellow", "cigars"))

    # 7. The German smokes Pipe.
    problem.add_constraint(SameHouseConstraint("German", "pipe"))

    # 8. Already taken care of.

    # 9. The man who smokes lights has a neighbour who drinks water.
    problem.add_constraint(NextHouseConstraint("lights", "water"))
    # problem.add_constraint(NextToConstraint("water", "lights"))

    # 10. The person who smokes No filter has birds.
    problem.add_constraint(SameHouseConstraint("no filter", "birds"))

    # 11. The Swede keeps dogs as pets.
    problem.add_constraint(SameHouseConstraint("Swede", "dogs"))

    # 12. The Norwegian lives next to the blue house.
    problem.add_constraint(NextHouseConstraint("Norwegian", "blue"))
    problem.add_constraint(NextHouseConstraint("blue", "Norwegian"))

    # 13. The man who keeps horses lives next to the Yellow house.
    problem.add_constraint(NextHouseConstraint("horses", "yellow"))
    # problem.add_constraint(NextToConstraint("yellow", "horses"))

    # 14. The man who smokes Menthol drinks beer.
    problem.add_constraint(SameHouseConstraint("menthol", "beer"))

    # 15. The owner of the Green house drinks coffee.
    problem.add_constraint(SameHouseConstraint("green", "coffee"))

    return problem


def print_nice_result(res):
    _colors = list(range(5))
    _nationalities = list(range(5))
    _drinks = list(range(5))
    _smokes = list(range(5))
    _pets = list(range(5))
    for i in range(5):
        print(f'House {i+1}'.ljust(15), end=' ')
    print()
    for k, v in res.items():
        if k in NATIONALITIES:
            _nationalities[v] = k
        if k in COLORS:
            _colors[v] = k
        if k in DRINKS:
            _drinks[v] = k
        if k in SMOKES:
            _smokes[v] = k
        if k in PETS:
            _pets[v] = k

    def print_5(values):
        for index in range(5):
            print(values[index].ljust(15), end=' ')
        print()

    print_5(_nationalities)
    print_5(_colors)
    print_5(_drinks)
    print_5(_smokes)
    print_5(_pets)


if __name__ == '__main__':
    einstein_problem = define_problem()
    logging.info(f"____________EINSTEIN____________")
    solver = CSPSolver(
        problem=einstein_problem,
        algorithm_type=AC3,
        variable_selector=DegreeVariableSelector,
        value_selector=LeastConstrainingValueSelector,
        use_ac3=True
    )
    result = solver.get_solution()
    print_nice_result(result)
