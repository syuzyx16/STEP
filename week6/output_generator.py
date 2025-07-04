from common import format_tour, read_input

import sys
import solver_greedy
import solver_random
import solver_aco
import solver_aco_lite2opt


CHALLENGES = 7

solvers = {
    'greedy': solver_greedy,
    'random': solver_random,
    'aco': solver_aco,
    'aco_lite' : solver_aco_lite2opt
}

def generate_output(solver):
    for i in range(5,CHALLENGES):
        cities = read_input(f'input_{i}.csv')
        tour = solver.solve(cities)
        with open(f'output_{i}.csv', 'w') as f:
            f.write(format_tour(tour) + '\n')


if __name__ == '__main__':
    assert len(sys.argv) > 1
    solver_name = sys.argv[1]
    solver = solvers[solver_name]
    generate_output(solver)