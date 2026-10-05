# Guion para el video (aproximadamente 5 a 7 minutos)

Las indicaciones entre corchetes son acciones en pantalla.

## 1. Presentacion

[Mostrar la carpeta Lab8_TC.]

Hola, soy Sebastian Lemus, carne 241155. Presentare los ejercicios programables del Laboratorio 8 de Teoria de la Computacion, el analisis de complejidad y las mediciones de ejecucion.

En programas estan las implementaciones, las tablas y las graficas. Los ejercicios a mano estan en ejercicios_a_mano.

## 2. Ejecucion

[Abrir PowerShell y ejecutar:]

```powershell
cd "C:\Users\Brenda\Desktop\app\Lab8_TC\programas"
python problem1.py 10
python problem2.py 10
python problem3.py 10
python profile.py
```

Primero muestro cada programa con una entrada pequena. El primero devuelve su contador y los otros dos imprimen Sequence.

El profiling intenta las siete entradas solicitadas: 1, 10, 100, 1000, 10000, 100000 y 1000000. Ejecuta los ciclos originales en procesos separados. Mide el tiempo dentro de la funcion con un reloj de alta resolucion, sin incluir el arranque de Python.

Para los problemas 2 y 3 conserva las llamadas a print, pero redirige la salida al dispositivo nulo. Asi se mide la ejecucion con esa condicion, sin llenar la pantalla. No se mide el costo de mostrar millones de lineas en una terminal.

Cada proceso tiene un limite de diez segundos. Cuando lo supera, se termina y queda marcado como limite excedido, sin asignarle un tiempo estimado. El limite incluye el arranque del proceso. Se puede ampliar con la opcion --timeout.

## 3. Problema 1

[Mostrar problem1.py y graficas/problema1.svg.]

El primer y segundo ciclo tienen una cantidad de iteraciones proporcional a n. El tercero duplica k en cada paso y realiza aproximadamente logaritmo en base dos de n iteraciones. Al multiplicar los factores, la complejidad es O de n al cuadrado por logaritmo de n.

El conteo exacto para n igual a un millon es de 5,000,010,000,000 incrementos. Esa entrada se intenta, pero no termina dentro del limite. La grafica muestra solamente las entradas que terminaron.

## 4. Problema 2

[Mostrar problem2.py y graficas/problema2.svg.]

Aunque hay dos ciclos, el interno termina en su primera iteracion por el break. Se realiza una impresion por cada vuelta del ciclo externo. La complejidad es O de n. Para n menor o igual a uno, retorna inmediatamente.

## 5. Problema 3

[Mostrar problem3.py y graficas/problema3.svg.]

El primer ciclo recorre aproximadamente n dividido entre tres valores, y el segundo aproximadamente n dividido entre cuatro. El producto es proporcional a n al cuadrado dividido entre doce. Al omitir factores constantes, la complejidad es O de n al cuadrado.

Para n igual a un millon se requieren 83,333,250,000 impresiones. El limite de ejecucion permite registrar que esta entrada no termino, sin confundirla con una medicion completada.

## 6. Tablas y cierre

[Mostrar resultados/resumen.md y los CSV. Luego mostrar el PDF a mano.]

Las tablas incluyen la entrada, el conteo de operaciones, el tiempo medido si termino y el estado. Las graficas usan escala logaritmica en ambos ejes; no hay puntos para las entradas que excedieron el limite. Para entradas muy pequenas, el ruido de medicion puede impedir que los puntos sigan una curva ideal.

El problema 2 crece linealmente, el 3 cuadraticamente y el 1 cuadraticamente con un factor logaritmico. Las entradas con limite excedido quedan documentadas como ejecuciones incompletas; no son tiempos reales completos ni estimaciones.

Aqui estan los ejercicios resueltos a mano. El codigo y los resultados estan en el repositorio LAB8_TC. Gracias.

[Despues de subir el video a YouTube como no listado, agregar su enlace al README. Mantener el video por debajo de 10 minutos.]
