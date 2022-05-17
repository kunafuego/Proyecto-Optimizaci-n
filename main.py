#Para los resultados se debe crear un txt con los resultados. Es mejor que un pdf porque no necesita
#librerías externas. Hacer esto una vez que se esté seguro que los resultados están buenos.

from gurobipy import Model, GRB, quicksum
import random

#Cantidad de días
T = 30 
# Cantidad de productos
P = 100 


# Rangos
T_ = range(1, T + 1)
P_ = range(1, P + 1)
Q_ = ["R", "C", "A"]

# Parametros:

# Costo Fijo por hacer un pedido de p el día t

# Costo de una unidad de p en el día t.

# Precio por guardar una unidad del producto p en bodega desde el dıa t al t + 1

# Volumen máximo que se puede almacenar en la bodega del tipo de producto q

# Volumen que ocupa una unidad del producto p

# Demanda del producto p en el dıa t.
 
# Mınima cantidad que se puede pedir del producto p

# Volumen máximo que se puede transportar del producto p.

# Presupuesto inicial

# Precio de venta del producto p

# Cantidad de días para que se venza p después de haberlo comprado.

# Costo de desechar un producto p debido a que esta vencido.


############### MODELO ###############

model = Model()

#### Variables

# Cantidad comprada del producto p en el día t que vence en e días

# Cantidad vendida del producto p en el dıa t que vencıa en e dıas.

# Cantidad en el inventario del producto p al final del dıa t que vence en e dıas.

# Cantidad de p desechada al final del dıa t, porque vence en t + 1.

# Presupuesto del supermercado al final del dıa t, despues de haber pagado el bodegaje para la noche.


#### Función Objetivo

#### Restricciones

#R1 

#R2

#R3

#R4 

#R5
 
#R6 

#R7

#R8 

#R9 

#R10 

#R11 

#R12 

#R13 

#R14 

#R15 

#R16 

#R17 

#R18 

 



#### Imprimir resultados