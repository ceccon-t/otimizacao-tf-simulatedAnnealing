import os
import math 


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
    

# TODO: funcao para criar solucao inicial

# TODO: funcao para gerar vizinhanca

# TODO: funcao para avaliar funcao objetivo


def degree_on_original(v: int) -> int:
    """
        Calculate degree of vertex 'v' on original graph, probably more useful when generating original solution
    """
    global original_graph  # Vou pensar em algo melhor do que isso depois
    i = vtoi(v)
    return sum(original_graph[i])


def degree_on_solution(v: int, s: 'set[int]') -> int:
    """
        Calculate degree of vertex 'v' on solution 's'
    """
    global original_graph  # Vou pensar em algo melhor do que isso depois
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


# Parametros
# TODO: (talvez) permitir que sejam passados pela linha de comando
# Variavel do parametro     # Como esta escrito nos slides

initial_solution = set()    # s     : criar com algum algoritmo (guloso, etc.)
initial_temperature = 0.9   # Ti    : ideia proposta nos slides, mas tem que pensar se faz sentido e como implementar
final_temperature = 0.1     # Tf    : criterio de parada, mas pode usar outro tambem
iterations = 10             # I     : proporcional ao tamanho da vizinhanca
cooling_rate = 0.8          # r     : idealmente entre [0.8, 0.99]


def boltzmann(x: float, temperature: float) -> float:
    e = math.e
    exponent = - x / temperature
    return e ** exponent


# Algumas instancias de escala variada para facilitar testes
small_instance = 'induced_7_10.dat'
medium_instance = 'induced_200_5970.dat'
large_instance = 'induced_700_122325.dat'

# TODO: aceitar parametro passado na linha de comando com nome da instancia desejada
filename = small_instance

# Caminho completo ate arquivo da instancia utilizada
filepath = os.path.join('..', 'dados', 'instancias', filename)

# Cria matriz de adjacencia
# Variavel              # Como esta escrito nos slides
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


# Generate initial solution
# Add-1
for i in range(total_vertices):
    v = itov(i)
    tentative_solution = set(initial_solution)
    tentative_solution.add(v)
    if is_valid_solution_full(tentative_solution):
        initial_solution = set(tentative_solution)


# TODO: Logica do algoritmo


print('Matrix with original instance data:')
print(original_graph)

print(f'Initial solution: {initial_solution}')
print(f'Size of initial solution: {len(initial_solution)}')

print(f'Total number of verticies on instance: {total_vertices}')
print(f'Total number of edges on instance: {total_edges}')

print('Cest fini.')
