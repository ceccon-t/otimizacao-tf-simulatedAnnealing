Para rodar o script:
```
python3 simulatedAnnealing.py [-h] [--initial_temperature INITIAL_TEMPERATURE] [--final_temperature FINAL_TEMPERATURE] [--iterations ITERATIONS] [--cooling_rate COOLING_RATE]
                             [--metropolis_runs METROPOLIS_RUNS] [--log_to LOG_TO]
                             INDEX
```
Sendo que os podem ser passados os seguintes argumentos:

Argumentos obrigatorios:
  - INDEX:                 Indice do arquivo (0 para a primeira instância e 16 para a última)

Argumentos opcionais:
  - -h, --help:            Mensagem de ajuda
  - --initial_temperature INITIAL_TEMPERATURE, -it INITIAL_TEMPERATURE: Temperatura inicial
  - --final_temperature FINAL_TEMPERATURE, -ft FINAL_TEMPERATURE: Temperatura final
  - --iterations ITERATIONS, -i ITERATIONS: Número de iterações com temperatura constante do SA
  - --cooling_rate COOLING_RATE, -cr COOLING_RATE: Cooling rate do SA
  - --metropolis_runs METROPOLIS_RUNS, -mr METROPOLIS_RUNS: Número de iterações dentro do metropolis
  - --log_to LOG_TO, -lt LOG_TO: Diretório em que serão colocados os logs de execução, caso o flag seja passado

ex:
```
python3 simulatedAnnealing.py 2 -ft 0.5 -lt pasta_logs
```
