using JuMP
using Formatting
using Dates
using Gurobi

# verifica se o programa recebeu um argumento
if length(ARGS) != 1
    exit()
else
    filename = ARGS[1]
end

# abre o arquivo
println(filename)
f = open(filename, "r")
    
# le a quantidade de vertices
s = readline(f)         
N = parse(Int, split(s," ")[1])

# Matriz de adjacencia
A = zeros(Bool, N, N)
   
# le as arestas
while ! eof(f) 
    s = readline(f)         
    a, b = [parse(Int, num) for num in split(s, " ")]

    # coloca na matriz
    A[a, b] = 1
    A[b, a] = 1
end
close(f)

# Grau maximo de um vertice
M = (sum(A,dims=2))

# modelo
model = Model()
set_optimizer(model, Gurobi.Optimizer);
set_optimizer_attribute(model, "TimeLimit", 3600)
set_silent(model)

# variaveis
@variable(model, X[1:N], Bin);
@variable(model, Y[1:N], Int);

# objetivo
@objective(model, Max, sum(X[u] for u in 1:N))

# restricoes
@constraint(model, RMenor[u=1:N], sum(A[u,v]*X[v] for v in 1:N) <= 2*Y[u] + M[u] * (1-X[u]))
@constraint(model, RMaior[u=1:N], sum(A[u,v]*X[v] for v in 1:N) >= 2*Y[u] - M[u] * (1-X[u]))

# otimiza o modelo
optimize!(model)

# mostra informacoes sobre o modelo
@show solution_summary(model)
println("Vertices escolhidos: ",findall(x->x==1, value.(X)))
