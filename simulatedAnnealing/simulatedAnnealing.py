import os
import math 
import random
import time
from datetime import datetime


######################################################
####  HELPER FUNCTIONS ###############################
######################################################


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


def log_results(filename: str, results: dict, temp: bool) -> None:
    full_filename = filename + '_-_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log'
    folder_name = 'tmp' if temp else 'log'

    content = ''
    if 'instance' in results:
        content = content + 'Instance: ' + str(results['instance']) + '\n'
    
    content = content + '\nParameters: ' + '\n'
    if 'initial_temperature' in results:
        content = content + 'Initial temperature: ' + str(results['initial_temperature']) + '\n'
    if 'final_temperature' in results:
        content = content + 'Final temperature: ' + str(results['final_temperature']) + '\n'
    if 'iterations' in results:
        content = content + 'Iterations: ' + str(results['iterations']) + '\n'
    if 'cooling_rate' in results:
        content = content + 'Cooling rate: ' + str(results['cooling_rate']) + '\n'
    if 'metropolis_runs' in results:
        content = content + 'Metropolis runs: ' + str(results['metropolis_runs']) + '\n'
    
    content = content + '\nResults: ' + '\n'
    if 'total_time' in results:
        content = content + 'Time to run: ' + str(results['total_time']) + ' (seconds)' + '\n'
    if 'initial_solution' in results:
        content = content + 'Initial solution: ' + str(results['initial_solution']) + '\n'
        content = content + 'Size of initial solution: ' + str(len(results['initial_solution'])) + '\n'
    if 'best_solution' in results:
        content = content + 'Best solution found: ' + str(results['best_solution']) + '\n'
        content = content + 'Size of best solution found: ' + str(len(results['best_solution'])) + '\n'

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    filepath = os.path.join(folder_name, full_filename)
    with open(filepath, 'w') as logfile:
        logfile.write(content)


def build_original_graph(filename: str) -> 'list[list[int]]':
    """
        Builds and return the graph that is described on file 'filename' inside instances folder
    """
    # Full path to file containing instance
    filepath = os.path.join('..', 'dados', 'instancias', filename)

    original_graph = [[]]

    with open(filepath, 'r') as instance:
        header = instance.readline()
        total_vertices, total_edges = parse_int_pair(header)

        original_graph = [[0 for j in range(total_vertices)] for i in range(total_vertices)]
        
        for _ in range(total_edges):
            v1, v2 = parse_int_pair(instance.readline())
            i = vtoi(v1)
            j = vtoi(v2)
            add_edge(original_graph, i, j)
    
    return original_graph 


######################################################
####  ALGORITHM FUNCTIONS  ###########################
######################################################

def boltzmann(x: float, temperature: float) -> float:
    """
        Probability of picking a solution with delta 'x' that is worse than current best one
    """
    e = math.e
    exponent = - x / temperature
    return e ** exponent


def build_initial_solution(all_vertices: 'set[int]') -> 'set[int]':
    initial_solution = set()
    total_vertices = len(all_vertices)
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
    return initial_solution


def neighborhood_1flip(s: 'set[int]') -> 'set[int]':
    # Chooses a random vertex and 'flips' it, that is
    #   if is in solution, remove it
    #   if is not in solution, adds it
    global all_vertices
    chosen = random.choice(list(all_vertices))
    flipped = itov(chosen)
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


def simulated_annealing(s: 'set[int]', Ti: float, Tf: float, I: int, r: float, metropolis_runs: int) -> 'set[int]':
    best_solution = s 
    current_solution = s
    best_value = even_degree_total(best_solution)
    temperature = Ti
    final_temperature = Tf
    cooling_rate = r

    while temperature >= final_temperature:
        print(f'Running iterations for temperature {temperature}')
        print(f'Current best solution has value: {best_value}')
        # Some iterations with constant T
        for _ in range(I):
            current_solution = metropolis(current_solution, temperature, metropolis_runs)
            current_value = even_degree_total(current_solution)
            # print(f'Cur value: {current_value}, best value: {best_value} ')
            if current_value > best_value:
                # print(f'Found better')
                best_solution = current_solution
                best_value = current_value

        temperature = cooling_rate * temperature

    return best_solution


######################################################
####  SETUP AND RUN  #################################
######################################################

_ALL_INSTANCES_FILENAMES = [
    'induced_7_10.dat',         # 0
    'induced_10_22.dat',        # 1
    'induced_50_122.dat',       # 2
    'induced_50_368.dat',       # 3
    'induced_50_612.dat',       # 4
    'induced_100_495.dat',      # 5
    'induced_100_1485.dat',     # 6
    'induced_100_2475.dat',     # 7
    'induced_200_1990.dat',     # 8
    'induced_200_5970.dat',     # 9
    'induced_200_9950.dat',     # 10
    'induced_500_12475.dat',    # 11
    'induced_500_37425.dat',    # 12
    'induced_500_62375.dat',    # 13
    'induced_700_24465.dat',    # 14
    'induced_700_73395.dat',    # 15
    'induced_700_122325.dat'    # 16
]

# Some instances of varying scale to facilitate tests
small_instance = _ALL_INSTANCES_FILENAMES[0] # 'induced_7_10.dat'
medium_instance = _ALL_INSTANCES_FILENAMES[9] # 'induced_200_5970.dat'
large_instance = _ALL_INSTANCES_FILENAMES[16] #'induced_700_122325.dat'

# TODO: (maybe) accept this parameter from command line with name of desired instance file
filename = medium_instance

instances_to_run = _ALL_INSTANCES_FILENAMES[14:]

for instance in instances_to_run:
    # Create adjacency matrix and related data
    original_graph = build_original_graph(instance)
    total_vertices = len(original_graph[0])
    all_vertices = set(range(total_vertices))


    # Parameters
    # TODO: (maybe) allow these to be passed from  command line
    # Parameter variable        # How it is written on slides
    initial_solution = set()    # s     : create with some algorithm (greedy, etc.)
    initial_temperature = 0.99  # Ti    : check if we should use idea proposed on slides or something else
    final_temperature = 0.2     # Tf    : end criteria, but we can use another one as well
    iterations = total_vertices             # I     : ideally proportional to size of neighborhood
    cooling_rate = 0.99          # r     : ideally in range [0.8, 0.99]
    metropolis_runs = 50       # how many times should the Metropolis algorithm run for each iteration with fixed temperature


    # RUN SIMULATED ANNEALING
    initial_time = time.time()
    initial_solution = build_initial_solution(all_vertices)

    best_solution = simulated_annealing(initial_solution, initial_temperature, final_temperature, iterations, cooling_rate, metropolis_runs)
    final_time = time.time()
    total_time = final_time - initial_time

    # Info about initial solution
    print(f'Initial solution: {initial_solution}')
    print(f'Size of initial solution: {len(initial_solution)}')

    # Info about best found solution
    print(f'Best solution found: {best_solution}')
    print(f'Value of best solution: {even_degree_total(best_solution)}') 
    print(f'Size of best solution found: {len(best_solution)}')  # Hopefully the same as above :P

    # Execution time
    print(f'Total time to run this instance: {total_time} (seconds)')

    should_log = True 

    if should_log:
        infos = dict()
        infos['instance'] = instance
        infos['total_time'] = total_time
        infos['initial_solution'] = initial_solution
        infos['initial_temperature'] = initial_temperature
        infos['final_temperature'] = final_temperature
        infos['iterations'] = iterations
        infos['cooling_rate'] = cooling_rate
        infos['metropolis_runs'] = metropolis_runs
        infos['best_solution'] = best_solution 

        log_to_temp = True

        log_file = instance.replace('.dat', '')


        log_results(log_file, infos, log_to_temp)    


print('Cest fini.')
