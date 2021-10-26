import os
import math 

e = math.e


def vtoi(v: int) -> int:
    """
        Converte de numero de vertice (1-indexed) para seu indice na matriz de adjacencia (0-indexed)
    """
    return v - 1


def itov(i: int) -> int:
    """
        Converte de numero do indice na matriz de adjacencia (0-indexed) para o numero do vertice (1-indexed)
    """
    return i + 1


def parse_int_pair(s: str) -> 'tuple[int]':
    """
        Dada uma string no formato "A B", com A e B numeros inteiros retorna tupla com inteiros A e B nessa ordem
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

# TODO: (talvez) funcao para calcular grau de um vertice no grafo original

# TODO: funcao para calcular grau de um vertice em uma solucao especifica


# Parametros
# TODO: (talvez) permitir que sejam passados pela linha de comando
# Variavel do parametro     # Como esta escrito nos slides

initial_solution = set()    # s     : criar com algum algoritmo (guloso, etc.)
initial_temperature = 0.9   # Ti    : ideia proposta nos slides, mas tem que pensar se faz sentido e como implementar
final_temperature = 0.1     # Tf    : criterio de parada, mas pode usar outro tambem
iterations = 10             # I     : proporcional ao tamanho da vizinhanca
cooling_rate = 0.8          # r     : idealmente entre [0.8, 0.99]


def boltzmann(x: float, temperature: float) -> float:
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

# Preenche matriz com dados da instancia
with open(filepath, 'r') as instancia:
    header = instancia.readline()
    total_vertices, total_edges = parse_int_pair(header)

    original_graph = [[0 for j in range(total_vertices)] for i in range(total_vertices)]
    
    for aresta in range(total_edges):
        v1, v2 = parse_int_pair(instancia.readline())
        i = vtoi(v1)
        j = vtoi(v2)
        add_edge(original_graph, i, j)

    for i in range(total_vertices):
        print(f'Vertex {itov(i)}')

    


print('Matriz com dados originais da instancia:')
print(original_graph)

print(f'Total de vertices na instancia: {total_vertices}')
print(f'Total de arestas na instance: {total_edges}')

print('Cest fini.')
