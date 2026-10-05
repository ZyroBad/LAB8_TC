# Laboratorio 8 - Teoria de la computacion

Repositorio para el Laboratorio 8.

## Contenido

- `programas/`: implementaciones instrumentadas de los problemas 1, 2 y 3.
- `programas/resultados/`: tablas CSV con input, operaciones y tiempos.
- `programas/graficas/`: graficas SVG de input contra tiempo estimado en escala log-log.
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

Los programas se implementaron con contadores para medir el trabajo sin imprimir millones de lineas. Para los valores grandes de `n`, ejecutar literalmente los ciclos de los problemas 1 y 3 seria impractico, porque sus crecimientos son `O(n^2 log n)` y `O(n^2)`.

Por eso `profile.py` calcula el numero exacto de operaciones principales y usa una calibracion local de operaciones por segundo para estimar el tiempo de ejecucion. Tambien registra el tiempo real que toma calcular la formula exacta.

## Complejidades

| Problema | Complejidad |
| --- | --- |
| 1 | `O(n^2 log n)` |
| 2 | `O(n)` |
| 3 | `O(n^2)` |

## Video

Enlace de YouTube no listado: pendiente de agregar despues de grabar y subir el video.

El guion se dejo en el chat de entrega para copiarlo al momento de grabar.
