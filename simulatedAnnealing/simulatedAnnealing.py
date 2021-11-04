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


def get_initial_solution_gurobi(instance: str) -> 'set[int]':
    GUROBI_SOLUTIONS = {
        'induced_7_10.dat': set([1, 3, 4, 6, 7]),
        'induced_10_22.dat': set([1, 2, 3, 6, 7, 8, 9, 10]),
        'induced_50_122.dat': set([5, 6, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 24, 25, 27, 28, 29, 30, 31, 33, 37, 38, 39, 40, 41, 42, 43, 44, 45, 47, 49, 50]),
        'induced_50_368.dat': set([1, 2, 3, 4, 5, 6, 9, 10, 12, 15, 16, 17, 18, 19, 20, 24, 26, 27, 28, 29, 30, 31, 33, 34, 35, 36, 37, 38, 39, 40, 42, 43, 44, 45, 47, 49, 50]),
        'induced_50_612.dat': set([1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 15, 17, 19, 21, 22, 23, 25, 26, 28, 30, 31, 33, 35, 36, 37, 38, 41, 44, 45, 48, 49, 50]),
        'induced_100_495.dat': set([2, 5, 6, 8, 9, 11, 13, 21, 23, 24, 25, 28, 30, 32, 33, 34, 36, 37, 38, 39, 40, 41, 42, 44, 46, 47, 48, 49, 50, 52, 54, 55, 57, 58, 59, 60, 61, 62, 63, 64, 67, 68, 69, 73, 74, 76, 78, 80, 82, 83, 84, 87, 88, 89, 92, 93, 95, 96, 97, 98, 99, 100]),
        'induced_100_1485.dat': set([1, 3, 5, 7, 8, 9, 10, 19, 21, 23, 24, 25, 27, 30, 41, 43, 47, 48, 51, 59, 60, 65, 67, 68, 70, 72, 75, 76, 77, 79, 82, 84, 85, 88, 89, 95, 96, 98, 100]),
        'induced_100_2475.dat': set([1, 21, 22, 27, 30, 31, 33, 34, 35, 43, 44, 45, 46, 50, 56, 60, 61, 69, 71, 73, 81, 82, 83, 86, 90, 92, 93, 96, 97, 99, 100]),
        'induced_200_1990.dat': set([2, 3, 4, 5, 6, 12, 15, 19, 23, 29, 30, 31, 32, 33, 41, 43, 44, 56, 57, 58, 60, 66, 70, 71, 73, 74, 84, 86, 93, 101, 110, 112, 114, 117, 119, 120, 122, 123, 125, 132, 134, 135, 141, 142, 144, 146, 149, 151, 153, 157, 161, 162, 164, 173, 174, 187, 188, 198, 200]),
        'induced_200_5970.dat': set([1, 5, 9, 12, 14, 24, 29, 33, 35, 42, 48, 59, 64, 65, 66, 67, 74, 75, 90, 96, 107, 109, 112, 121, 123, 124, 131, 133, 134, 140, 150, 152, 174, 182, 187, 191, 195, 196]),
        'induced_200_9950.dat': set([1, 8, 12, 17, 18, 23, 25, 27, 30, 87, 88, 89, 94, 97, 108, 113, 120, 123, 130, 145, 146, 153, 154, 165, 166, 188, 189, 190, 193, 197]),
        'induced_500_12475.dat': set([4, 8, 13, 19, 24, 31, 34, 44, 57, 65, 67, 69, 80, 89, 96, 107, 110, 111, 115, 121, 123, 127, 135, 137, 148, 165, 166, 168, 170, 171, 176, 185, 187, 190, 191, 206, 208, 231, 232, 233, 248, 261, 267, 270, 276, 283, 295, 315, 323, 334, 341, 344, 351, 377, 382, 391, 404, 415, 419, 440, 444, 445, 450, 454, 463, 466, 470, 475, 494, 497, 498]),
        'induced_500_37425.dat': set([3, 7, 8, 12, 16, 17, 31, 46, 50, 62, 65, 97, 99, 131, 162, 171, 172, 178, 230, 241, 244, 248, 265, 275, 326, 329, 385, 390, 423, 468, 484, 495]),
        'induced_500_62375.dat': set([1, 2, 6, 12, 18, 33, 48, 72, 76, 107, 118, 124, 147, 148, 150, 177, 190, 205, 232, 259, 286, 300, 314, 319, 370, 397, 448, 452, 488]),
        'induced_700_24465.dat': set([3, 4, 9, 17, 19, 22, 26, 27, 30, 32, 43, 58, 66, 76, 79, 80, 81, 87, 96, 99, 107, 114, 128, 144, 162, 170, 172, 173, 178, 185, 215, 241, 271, 275, 284, 290, 331, 335, 354, 356, 361, 378, 385, 393, 395, 417, 448, 451, 454, 455, 461, 468, 483, 496, 507, 519, 540, 559, 571, 576, 577, 591, 599, 607, 631, 664]),
        'induced_700_73395.dat': set([1, 3, 4, 7, 29, 31, 36, 59, 72, 110, 113, 161, 208, 216, 255, 289, 300, 356, 387, 422, 444, 486, 497, 498, 505, 574, 577, 579, 684]),
        'induced_700_122325.dat': set([1, 2, 6, 20, 37, 54, 77, 121, 131, 141, 181, 237, 329, 343, 350, 352, 367, 379, 442, 509, 619, 675]),
    } 
    return GUROBI_SOLUTIONS[instance]


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

instances_to_run = _ALL_INSTANCES_FILENAMES[8:]

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
    metropolis_runs = 1000       # how many times should the Metropolis algorithm run for each iteration with fixed temperature


    # RUN SIMULATED ANNEALING
    initial_time = time.time()
    #initial_solution = build_initial_solution(all_vertices)
    initial_solution = get_initial_solution_gurobi(instance)

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
