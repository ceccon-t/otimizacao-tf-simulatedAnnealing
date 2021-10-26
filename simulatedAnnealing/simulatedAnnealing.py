import os
import math 

e = math.e


def vtoi(v: int) -> int:
    """
        Converte de numero de vertice (1-indexed) para seu indice na matriz de adjacencia (0-indexed)
    """
    return v - 1


def parse_int_pair(s: str) -> 'tuple[int]':
    """
        Dada uma string no formato "A B", com A e B numeros inteiros retorna tupla com inteiros A e B nessa ordem
    """
    a, b = s.split(" ")
    a = int(a)
    b = int(b)
    return (a, b)


def adiciona_aresta(M, u, v):
    M[u][v] = 1
    M[v][u] = 1


def remove_aresta(M, u, v):
    M[u][v] = 0
    M[v][u] = 0
    

# TODO: funcao para criar solucao inicial

# TODO: funcao para gerar vizinhanca

# TODO: funcao para avaliar funcao objetivo

# TODO: (talvez) funcao para calcular grau de um vertice no grafo original

# TODO: funcao para calcular grau de um vertice em uma solucao especifica


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
A = [[]]
V = 0
E = 0

# Preenche matriz com dados da instancia
with open(filepath, 'r') as instancia:
    header = instancia.readline()
    V, E = parse_int_pair(header)

    A = [[0 for j in range(V)] for i in range(V)]
    
    for aresta in range(E):
        v1, v2 = parse_int_pair(instancia.readline())
        i = vtoi(v1)
        j = vtoi(v2)
        adiciona_aresta(A, i, j)


print('Matriz com dados originais da instancia:')
print(A)

print(f'Total de vertices na instancia: {V}')
print(f'Total de arestas na instance: {E}')

print('Cest fini.')
