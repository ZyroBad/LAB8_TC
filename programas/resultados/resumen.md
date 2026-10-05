# Resultados de profiling real

Limite por proceso: 10 s. Cada entrada se intenta una vez.
Tiempo medido dentro de la funcion, incluyendo flush de salida; excluye arranque de Python.
El limite incluye el arranque del proceso. Un limite excedido no es un tiempo medido ni una estimacion.
Las impresiones se ejecutan y se redirigen al dispositivo nulo; no se mide el renderizado de terminal.

## problema1 - O(n^2 log n)

| n | Operaciones | Tiempo medido (s) | Estado |
| --- | --- | --- | --- |
| 1 | 2 | 0.000027000031 | completado |
| 10 | 120 | 0.000045300054 | completado |
| 100 | 17850 | 0.003259400022 | completado |
| 1000 | 2505000 | 0.367842400039 | completado |
| 10000 | 350070000 | - | limite_excedido |
| 100000 | 42500850000 | - | limite_excedido |
| 1000000 | 5000010000000 | - | limite_excedido |

## problema2 - O(n)

| n | Operaciones | Tiempo medido (s) | Estado |
| --- | --- | --- | --- |
| 1 | 0 | 0.000010899967 | completado |
| 10 | 10 | 0.000095799973 | completado |
| 100 | 100 | 0.000994200003 | completado |
| 1000 | 1000 | 0.009327800013 | completado |
| 10000 | 10000 | 0.056763299974 | completado |
| 100000 | 100000 | 0.576840299997 | completado |
| 1000000 | 1000000 | 5.776884699997 | completado |

## problema3 - O(n^2)

| n | Operaciones | Tiempo medido (s) | Estado |
| --- | --- | --- | --- |
| 1 | 0 | 0.000012700038 | completado |
| 10 | 9 | 0.000084400002 | completado |
| 100 | 825 | 0.004417999997 | completado |
| 1000 | 83250 | 0.475600700011 | completado |
| 10000 | 8332500 | - | limite_excedido |
| 100000 | 833325000 | - | limite_excedido |
| 1000000 | 83333250000 | - | limite_excedido |
