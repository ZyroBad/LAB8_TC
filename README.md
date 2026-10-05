# Laboratorio 8 - Teoria de la computacion

Repositorio para el Laboratorio 8.

## Contenido

- `programas/`: implementaciones de los problemas 1, 2 y 3 y profiling real.
- `programas/resultados/`: tablas CSV con input, operaciones y tiempos.
- `programas/graficas/`: graficas SVG de input contra tiempo medido en escala log-log.
- `programas/resultados/resumen.md`: tablas legibles y condiciones de medicion.
- `ejercicios_a_mano/Lab8_TC_Sebastian_Lemus_241155.pdf`: PDF con los ejercicios hechos a mano.

## Requisitos

- Python 3.10 o superior.

No se necesitan librerias externas para ejecutar el profiling ni para generar las graficas SVG.

## Ejecucion

Desde la raiz del repositorio:

```bash
cd programas
python profile.py
```

El script genera:

- `programas/resultados/problema1.csv`
- `programas/resultados/problema2.csv`
- `programas/resultados/problema3.csv`
- `programas/graficas/problema1.svg`
- `programas/graficas/problema2.svg`
- `programas/graficas/problema3.svg`

## Nota sobre el profiling

Se ejecutan los ciclos originales. Los problemas 2 y 3 imprimen `Sequence` en cada iteracion correspondiente. Durante el profiling, esas impresiones se redirigen al dispositivo nulo para evitar llenar la terminal o generar archivos enormes. El tiempo incluye las llamadas a `print` y el vaciado del buffer, pero no el renderizado de texto en una terminal.

Cada una de las siete entradas se intenta en un proceso separado. Se mide con `time.perf_counter()` la ejecucion de la funcion; se excluyen la importacion y el arranque de Python. El limite por proceso es de 10 segundos e incluye el arranque. Si se supera, el proceso se termina y la fila se marca `limite_excedido`, sin inventar un tiempo. Las graficas solo muestran ejecuciones completadas. Los conteos exactos de operaciones se calculan aparte y no sustituyen las mediciones.

Para aumentar el limite por entrada, ejecute `python profile.py --timeout 60`. Los tiempos dependen del equipo y las entradas pequenas pueden presentar ruido. El problema 1 para n=1000000 requiere 5000010000000 incrementos y el problema 3 requiere 83333250000 impresiones; por eso algunas entradas quedan incompletas bajo el limite. Estos casos no satisfacen una medicion completa de esas entradas y se documentan expresamente.

Para reintentar solamente entradas sin completar, conservando los tiempos existentes:

```bash
python profile.py --resume --timeout 120
```

Para permitir que todas las entradas pendientes terminen sin limite automatico:

```bash
python profile.py --resume --timeout 0
```

Este ultimo modo puede tardar dias. No cambia los ciclos ni reemplaza ejecuciones por formulas. Se guarda el CSV despues de cada intento terminado. Puede seleccionar entradas, por ejemplo `python profile.py --resume --timeout 120 --values 10000`. `Ctrl+C` interrumpe el intento actual; las filas ya guardadas se conservan y `--resume` permite continuar. Sin `--resume` se inicia una medicion nueva. Las filas con `pendiente` o `limite_excedido` no tienen tiempo completo; no deben presentarse como mediciones terminadas.

En los resultados incluidos, el problema 2 completo las siete entradas. Los problemas 1 y 3 completaron hasta n=10000, con tiempos de aproximadamente 54.65 s y 40.79 s respectivamente para esa entrada. n=100000 y n=1000000 siguen sin medicion completa en esos dos problemas. No se afirma cumplimiento total del apartado de profiling mientras falten esos tiempos.

Para ejecutar las pruebas: `python -m unittest discover -s programas -p test_programas.py -v` desde la raiz del repositorio.

Para mostrar los programas individuales: `python problem1.py 10`, `python problem2.py 10` y `python problem3.py 10`. Use valores pequenos al mostrar impresiones en pantalla.

## Complejidades

| Problema | Complejidad |
| --- | --- |
| 1 | `O(n^2 log n)` |
| 2 | `O(n)` |
| 3 | `O(n^2)` |

## Video
https://youtu.be/dHjncKzMDNo
