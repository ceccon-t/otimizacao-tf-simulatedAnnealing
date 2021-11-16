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

Caso seja passado algum valor para o argumento log_to (alternativamente, -lt), serão salvos em um diretório cujo nome é igual ao valor passado dois arquivos de mesmo nome (no formato <instancia_processada>-<data_e_horario>), mas extensões diferente. Segue uma breve descrição deles:

Arquivo *.log:

Arquivo textual que contém um log das principais informações a respeito da execução do Simulated Annealing. A primeira linha indica qual o nome da instância utilizada. Na sequência há uma série de linhas informando os valores dos parâmetros utilizados (temperatura inicial, temperatura final, etc.). Por fim, há uma série de linhas informando os resultados da execução, como por exemplo o tempo que o algoritmo levou para chegar ao final, a melhor solução encontrada (representada como um conjunto de vértices, por exemplo: {1, 2, 3} significaria que a melhor solução encontrada foi um subgrafo induzido contendo os vértices 1, 2 e 3) e o tamanho dessa solução. A última linha se refere aos dados usados para gerar o gráfico (segundo arquivo gerado) da execução.

Arquivo *.jpg:

Imagem no formato JPG que contém um gráfico mostrando o tamanho da melhor solução encontrada (eixo y) a cada iteração da função 'simulated_annealing' (eixo x). Para fins de legibilidade, o gráfico é cortado na iteração onde o tamanho da melhor solução parou de mudar. Ou seja, se o algoritmo executou por exemplo 1600 iterações, sendo que o tamanho da melhor solução encontrada estagnou em 15 a partir da iteração 14, o gráfico só mostra o intervalo da primeira iteração até a iteração 14.
