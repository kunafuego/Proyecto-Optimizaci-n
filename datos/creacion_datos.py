# -*- coding: utf-8 -*-
"""creacion_datos.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pfk2kUZ9Mw5XmctqBZk8EVVmWDwOW-QJ

# Creación de Datos Entrega 2

En este archivo se crearán los datos que se utilizarán para simular el modelo del proyecto. Esta simulación se resolverá con la ayuda de pygurobi, una librería open source de python.

En este archivo jupyter se hará uso de la librería *pandas*(no necesita que se descargue) para darle valores a los parámetros necesarios para la simulación. Estos serán guardados en DataFrames de la librería, y luego serán pasados a diccionarios de python. Cada uno de los parametros tendrá su propio diccionario, los cuales serán después leídos desde el archivo `main.py`.

Cabe mencionar que se intentó utilizar datos de empresas reales, pero estas no estuvieron dispuestas a colaborar por temas de confidencialidad empresarial.

Se simularán **100 productos** para un espacio de **28 días**, lo que serían 4 semanas completas comenzando desde el lunes.

## Parámetros

Existen básicamente dos tipos de parámetros. Los primeros son los que tienen como sufijo p(producto) y t(días), y otros que tienen como sufijo solo p. Por lo tanto, se creará un archivo .csv para cada uno de estos pares de parametros.

Acá solo nos faltarían los parametros V<sub>q</sub> y PR. Dado que son solo 4 datos que se deben simular, se calcularán los valores aleatoriamente en rangos que nos parezcan razonables, para que luego se ocupen estos mismos valores en el archivo `main.py`

### Parámetros con sufijo <sub>pt</sub>

Comenzaremos por crear un DataFrame que tenga una fila para cada par (p,t)
"""

import pandas
import random
df_pt = pandas.DataFrame({"p": [x for x in range(1,101)]*28}).sort_values("p")
df_pt.insert(1, "t", [x for x in range(1,29)]*100)

"""#### F<sub>pt</sub>

Este parametro indica el costo fijo por hacer un pedido del producto *p* en el día *t*.
Asumiremos que este costo solo varía por día de semana. Así, en el día 1 (primer lunes) y en el día 8 (segundo lunes) el costo fijo por pedir el producto *p* será el mismo. Se utiliza este supuesto porque en la vida real es así, pues las semanas son muy parecidas entre ellas en cuanto a temas de logística

Para cada producto *p* se comenzará calculando un costo fijo representativo, cuyo valor variará entre $20.000 y $30.000 para cada producto *p*. Para hacerlo más realista aun, los precios
de los costos fijos del producto *p* no podrán variar más de un 10% del costo fijo representativo.
"""

costos_fijos = list()
for p in range(100):
    valor_representativo_p = random.randint(20000, 30000)
    costos_fijos_p = list()
    for t in range(7):
        costos_fijos_p.append(random.randint(int(valor_representativo_p*0.9), int(valor_representativo_p*1.1)))
    costos_fijos.extend(costos_fijos_p*4)
df_pt.insert(2, "F", costos_fijos)

"""### n<sub>pt</sub>

Este parametro indica el costo de una unidad de *p* en el día *t*. Nuevamente asumiremos que para cada día de la semana, el producto va valer lo mismo en distintas semanas.

El valor representativo de este parametro variará entre $1.000 y $5.000. Luego, el valor para cada día de la semana no podrá variar más de un 10% del valor representativo.
"""

costos_unitarios = list()
for p in range(100):
    valor_representativo_p = random.randint(1000, 5000)
    costos_unitarios_p = list()
    for t in range(7):
        costos_unitarios_p.append(random.randint(int(valor_representativo_p*0.9), int(valor_representativo_p*1.1)))
    costos_unitarios.extend(costos_unitarios_p*4)
df_pt.insert(3, "n", costos_unitarios)

"""### b<sub>pt</sub>

Este parametro indica el costo de guardar en bodega una unidad del producto *p* desde el día *t* hasta *t+1*. Nuevamente asumiremos que para cada día de la semana, el costo de bodegaje va se el mismo en distintas semanas.

El valor representativo de este parametro variará entre $100 y $500. Luego, el valor para cada día de la semana no podrá variar más de un 10% del valor representativo.
"""

costos_bodegaje = list()
for p in range(100):
    valor_representativo_p = random.randint(100, 500)
    costos_bodegaje_p = list()
    for t in range(7):
        costos_bodegaje_p.append(random.randint(int(valor_representativo_p*0.9), int(valor_representativo_p*1.1)))
    costos_bodegaje.extend(costos_bodegaje_p*4)
df_pt.insert(4, "b", costos_bodegaje)

"""### d<sub>pt</sub>

Este parametro indica la demanda del producto *p* en el día *t*. En este caso no asumiremos que la demanda semana a semana es igual, porque pueden haber sucesos como fiestas nacionales que hacen variar bruscamente la demanda por ciertos bienes.

El valor de este parametro variará entre 50 y 100 unidades diarias. No existe restricción de variación.
"""

df_pt.insert(5, "d", [random.randint(5,10) for x in range(2800)])

"""## Parámetros con sufijo <sub>p</sub>"""

df_p = pandas.DataFrame({"p": [x for x in range(1,101)]}).sort_values("p")

"""### v<sub>p</sub>

Este parametro considera el volumen ocupado por una unidad de *p*. Se tomará un valor aleatorio entre 0.001 m^3 y 0.003 m^3.
"""

df_p.insert(1, "v", [random.uniform(0.001, 0.003) for _ in range(100)])

"""### maxc<sub>p</sub>

Este parámetro indica el volumen máximo que se puede transportar en un pedido del producto *p*.

Esto simula el espacio de los camiones del proveedor del producto *p* que dejan para transportar productos *p*.

Este tomará un valor aleatorio entre 5 y 7.5 m^3, lo cual serán 1.666 unidades de *p* en el peor caso, y 7.500 en el mejor.
"""

df_p.insert(2, "maxc", [random.uniform(5,7.5) for _ in range(100)])

"""### minc<sub>p</sub>

Este parámetro indica la mínima cantidad de productos de *p* que se deben pedir en un pedido de *p*.

Tomará un valor aleatorio entre 20 y 30 unidades.
"""

df_p.insert(3, "minc", [random.randint(20,30) for _ in range(100)])

"""### z<sub>p</sub>

Este parámetro indica el precio de venta del producto *p*. Este se calculará en función del máximo
costo unitario que tenga *p* en los 28 días. Luego, el precio de venta va a ser aleatoriamente entre un 10% y un 30%
mayor que este máximo costo unitario.
"""

precios_ventas = list()
for p in range(1,101):
    precios_compra_p = df_pt[df_pt["p"] == p]
    precio_venta_p = random.randint(int(precios_compra_p["n"].max()*1.1), int(precios_compra_p["n"].max()*1.3))
    precios_ventas.append(precio_venta_p)
df_p.insert(4, "z", precios_ventas)

"""### exp<sub>p</sub>

Este parámetro cuántos días faltan para que venza un producto *p* después de haberlo comprado.
Este tomará un valor entre 2 y 5 días.
"""

df_p.insert(5, "exp", [random.randint(4,10) for x in range(100)])

"""### u<sub>p</sub>

Este parámetro indica el costo monetario de desechar una unidad del producto *p*.
Este tomará un valor entre $10 y $100.
"""

df_p.insert(6, "u", [random.randint(10,100) for x in range(100)])

"""## Extras

### V<sub>q</sub>

Este parámetro indica qué volumen se puede almacenar en la bodega de los productos de tipo q. Estos se definirán directamente como diccionarios. Se define *q* como 3 subconjuntos de 
*p*. A(temperatura ambiente) van a ser 50 productos. R(refrigerados) otros 25 y C(congelados) los 25 restantes.

Existen tres tipos de productos *q*:
* Para los que están a temperatura ambiente, el volumen máximo será un valor aleatorio entre 150 y 170 m^3, lo que corresponderían a 170.000 unidades en el mejor caso y 1.000 en el peor. Esto será para los 50 productos *p* que están a temperatura ambiente.
* Para los congelados, el volumen máximo variará entre 75 y 90 m^3, lo que corresponderán a 1.000 unidades en el peor caso y 
* Para los refrigerados, el volumen máximo variará entre 75 y 90 m^3, lo que corresponderán a 1.000 unidades en el peor caso y
"""

A = [x for x in range(1,51)]
R = [x for x in range(51,75)]
C = [x for x in range(75,101)]
V = {"A": random.randint(150,170), "C": random.randint(75,90), "R": random.randint(75,90)}

"""### PR

Este parámetro indica el presupuesto inicial del supermercado, el cual será un valor entre $40.000.000 y $50.000.000.
"""

PR = random.randint(400000000, 500000000)

"""## Pasar los DataFrames a diccionarios"""

F = {(p,t): f for p,t,f in zip(df_pt["p"], df_pt["t"], df_pt["F"])}
n = {(p,t): n for p,t,n in zip(df_pt["p"], df_pt["t"], df_pt["n"])}
b = {(p,t): b for p,t,b in zip(df_pt["p"], df_pt["t"], df_pt["b"])}
d = {(p,t): d for p,t,d in zip(df_pt["p"], df_pt["t"], df_pt["d"])}
v = {p: v for p,v in zip(df_p["p"], df_p["v"])}
minc = {p: minc for p,minc in zip(df_p["p"], df_p["minc"])}
maxc = {p: maxc for p,maxc in zip(df_p["p"], df_p["maxc"])}
z = {p: z for p,z in zip(df_p["p"], df_p["z"])}
exp = {p: exp for p,exp in zip(df_p["p"], df_p["exp"])}
u = {p: u for p,u in zip(df_p["p"], df_p["u"])}

