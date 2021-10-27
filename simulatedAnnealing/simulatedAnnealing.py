import os
import math 
import random


# Some instances of varying scale to facilitate tests
small_instance = 'induced_7_10.dat'
medium_instance = 'induced_200_5970.dat'
large_instance = 'induced_700_122325.dat'

# TODO: accept this parameter from command line with name of desired instance file
filename = medium_instance

# Full path to file of instance being used
filepath = os.path.join('..', 'dados', 'instancias', filename)



def vtoi(v: int) -> int:
    """
        Converts from 1-indexed vertex 'name' to 0-indexed index on adjacency matrix
    """
    return v - 1


def itov(i: int) -> int:
    """
        Converts from 0-indexed index on adjacenct matrix to 1-indexed vertex 'name'
    """
    return i + 1


def parse_int_pair(s: str) -> 'tuple[int]':
    """
        Given a string with format "A B", with A and B being integers, returns tuple with ints A and B, in this order
    """
    a, b = s.split(" ")
    a = int(a)
    b = int(b)
    return (a, b)


def add_edge(M, u, v):
    M[u][v] = 1
    M[v][u] = 1


def remove_edge(M, u, v):
    M[u][v] = 0
    M[v][u] = 0
    

# TODO: function to generate neighborhood

def degree_on_original(v: int) -> int:
    """
        Calculate degree of vertex 'v' on original graph, probably more useful when generating original solution
    """
    global original_graph  # Maybe we can have this as a parameter, but need to check if that wouldnt add too much overhead
    i = vtoi(v)
    return sum(original_graph[i])


def degree_on_solution(v: int, s: 'set[int]') -> int:
    """
        Calculate degree of vertex 'v' on solution 's'
    """
    global original_graph  # Maybe we can have this as a parameter, but need to check if that wouldnt add too much overhead
    i = vtoi(v)
    degree = 0
    for u in s:
        j = vtoi(u)
        degree += original_graph[i][j]
    return degree


def is_valid_solution_full(s: 'set[int]') -> bool:
    """
        Checks if solution is valid by looking on original graph (not differential)
    """
    for v in s:
        deg = degree_on_solution(v, s)
        if deg % 2 != 0:
            return False
    return True 


def even_degree_total(s: 'set[int]') -> int:
    """
        Returns the number of vertices that have even degree on subgraph given by 's'
    """
    total = 0
    for v in s:
        deg = degree_on_solution(v, s)
        if deg % 2 == 0:
            total += 1
    return total


def boltzmann(x: float, temperature: float) -> float:
    """
        Probability of picking a solution with value 'x' that is worse than current best one
    """
    e = math.e
    exponent = - x / temperature
    return e ** exponent


def build_initial_solution():
    return set()


def neighborhood_1flip(s: 'set[int]') -> 'set[int]':
    # Chooses a random vertex and 'flips' it, that is
    #   if is in solution, remove it
    #   if is not in solution, adds it
    global all_vertices
    flipped = random.choice(list(all_vertices))
    neighbor = set(s)
    if flipped in neighbor:
        neighbor.remove(flipped)
    else:
        neighbor.add(flipped)
    return neighbor


def choose_neighbor(s: 'set[int]') -> 'set[int]':
    # Perhaps the best idea would be to have this as a generator...
    # Calls another function to facilitate testing different neighborhood
    #   strategies: we just need to create a new function and change what is called here
    return neighborhood_1flip(s) 


def metropolis(s: 'set[int]', temperature: float, runs: int) -> 'set[int]':
    best_found = set(s)
    best_value = even_degree_total(best_found)
    current = set(s)
    current_value = even_degree_total(current)
    for _ in range(runs):
        neighbor = choose_neighbor(current) # Choose neighbor
        
        neighbor_value = even_degree_total(neighbor)
        # print(f'Neighbor: {neighbor}, Value: {neighbor_value}')

        delta = neighbor_value - current_value
        if delta >= 0:  # our case is a maximization problem
            current = neighbor
            current_value = neighbor_value
            if current_value > best_value and is_valid_solution_full(current):
                best_found = current
                best_value = current_value
        else:
            random_value = random.random() 
            probability = boltzmann(-delta, temperature)
            if random_value < probability:
                current = neighbor
                current_value = neighbor_value
    return best_found 


def simulatedAnnealing(s: 'set[int]', Ti: float, Tf: float, I: int, r: float) -> 'set[int]':
    best_solution = s 
    current_solution = s
    best_value = even_degree_total(best_solution)
    temperature = Ti
    final_temperature = Tf
    cooling_rate = r

    while temperature >= final_temperature:
        print(f'Running iterations for temperature {temperature}')
        # Some iterations with constant T
        for _ in range(I):
            current_solution = metropolis(current_solution, temperature, 1000)
            current_value = even_degree_total(current_solution)
            # print(f'Cur value: {current_value}, best value: {best_value} ')
            if current_value > best_value:
                # print(f'Found better')
                best_solution = current_solution
                best_value = current_value

        temperature = cooling_rate * temperature

    return best_solution


# Create adjacency matrix
# Variable              # How it is written on slides
original_graph = [[]]   # A
total_vertices = 0      # V
total_edges = 0         # E

# Fill matrix with instance data
with open(filepath, 'r') as instancia:
    header = instancia.readline()
    total_vertices, total_edges = parse_int_pair(header)

    original_graph = [[0 for j in range(total_vertices)] for i in range(total_vertices)]
    
    for aresta in range(total_edges):
        v1, v2 = parse_int_pair(instancia.readline())
        i = vtoi(v1)
        j = vtoi(v2)
        add_edge(original_graph, i, j)

    # Some prints to test initialization of matrix and helper functions
    # all_vertices = set([i for i in range(total_vertices)])
    # print(all_vertices)
    # simple_solution_for_small = set([1,4,5])
    # for i in range(total_vertices):
    #     print(f'Vertice {itov(i)} tem grau {degree_on_original(itov(i))} no grafo original')
    #     print(f'Vertice {itov(i)} tem grau {degree_on_solution(itov(i), all_vertices)} em pseudo-solucao usando todos os vertices')
    #     print(f'Vertice {itov(i)} tem grau {degree_on_solution(itov(i), simple_solution_for_small)} em solucao com [1,4,5]')
    # print(f'Is {all_vertices} valid as a solution? : {is_valid_solution_full(all_vertices)}')
    # print(f'Is {simple_solution_for_small} valid as a solution? : {is_valid_solution_full(simple_solution_for_small)}')


all_vertices = set(range(total_vertices))


# Parameters
# TODO: (maybe) allow these to be passed from  command line
# Parameter variable        # How it is written on slides

initial_solution = set()    # s     : create with some algorithm (greedy, etc.)
initial_temperature = 0.99  # Ti    : check if we should use idea proposed on slides or something else
final_temperature = 0.2     # Tf    : end criteria, but we can use another one as well
iterations = 10             # I     : ideally proportional to size of neighborhood
cooling_rate = 0.99          # r     : ideally in range [0.8, 0.99]
metropolis_runs = 100       # how many times should the Metropolis algorithm run for each iteration with fixed temperature


# Generate initial solution

# Add-1
print('Starting Add-1: Trying to add single vertices on initial solution')
for i in range(total_vertices):
    v = itov(i)
    tentative_solution = set(initial_solution)
    tentative_solution.add(v)
    if is_valid_solution_full(tentative_solution):
        initial_solution = set(tentative_solution)
print(f'Finished Add-1, size of initial solution: {len(initial_solution)}')

# Add-2
use_add_2 = True    # Doesnt make any difference for small solution, makes small difference for medium and large solutions
if use_add_2:
    print('Starting Add-2: Trying to add pairs of vertices on initial solution')
    # print(f'All vertices: {all_vertices}')
    excluded_vertices = all_vertices.difference(initial_solution)
    for j in excluded_vertices:
        for i in excluded_vertices.difference(set([j])):
            v = itov(i)
            u = itov(j)
            tentative_solution = set(initial_solution)
            tentative_solution.add(v)
            tentative_solution.add(u)
            if is_valid_solution_full(tentative_solution):
                initial_solution = set(tentative_solution)
    print(f'Finished Add-2, size of initial solution: {len(initial_solution)}')



# SIMULATED ANNEALING
# initial_solution = build_initial_solution()
temperature = initial_temperature
solution = initial_solution
best_solution = initial_solution
best_value = even_degree_total(best_solution)

# temperatures_run = 0

best_solution = simulatedAnnealing(initial_solution, initial_temperature, final_temperature, iterations, cooling_rate)

# Show some info about instance
# print('Matrix with original instance data:')
# print(original_graph)

# print(f'Total number of vertices on instance: {total_vertices}')
# print(f'Total number of edges on instance: {total_edges}')


# Info about initial solution
print(f'Initial solution: {initial_solution}')
print(f'Size of initial solution: {len(initial_solution)}')

# Info about best found solution
# print(f'Went through {temperatures_run} different temperatures')
print(f'Best solution found: {best_solution}')
print(f'Value of best solution: {even_degree_total(best_solution)}') 
print(f'Size of best solution found: {len(best_solution)}')  # Hopefully the same as above :P

print('Cest fini.')
