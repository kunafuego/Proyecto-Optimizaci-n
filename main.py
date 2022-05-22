#Para los resultados se debe crear un txt con los resultados. Es mejor que un pdf porque no necesita
#librerías externas. Hacer esto una vez que se esté seguro que los resultados están buenos.

from gurobipy import Model, GRB, quicksum
import random

#Cantidad de días
T = 28 
# Cantidad de productos
P = 100 


# Rangos
T_ = range(0, T + 1)
E_ = range(1, T + 1)
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
c = model.addVars(P_, T_, E_)
# Si se decide comprar el producto p en el dia t
C = model.addVars(P_, T_)
# Cantidad vendida del producto p en el dıa t que vencıa en e dıas.
s = model.addVars(P_,T_,E_)
# Cantidad en el inventario del producto p al final del dıa t que vence en e dıas.
i = model.addVars(P_,T_,E_)
# Cantidad de p desechada al final del dıa t, porque vence en t + 1.
w = model.addVars(P_, T_)
# Presupuesto del supermercado al final del dıa t, despues de haber pagado el bodegaje para la noche.
B = model.addVars(T_)

#### Función Objetivo

objetivo = sum(sum(w[p,t] for p in P_) for t in T_)

#### Restricciones

#R1 
model.addConstrs(B[t] == B[t-1] + sum(sum(s[p,t,e]*z[p] for e in T_) for p in P_) -\
    sum(sum(c[p,t,e]*n[p,t] for e in T_) for p in P_) -\
    sum(w[p,t]*u[p] for p in P_) -\
    sum(sum(i[p,t,e] * b[p,t] for e in range(2, T + 1)) for p in P_) -\
    sum(C[p,t]*F[p,t] for p in P_) for t in range(2, T + 1))
#R2
model.addConst(B[1] == P*R) 
#Creo que era así cuando no dependía de subínices, REVISAR

#R3
model.addConstrs(c[p,t,e] <= C[p,t]*M for t in T_ for e in T_ for p in P)
#¿Cómo ponemos que M >> 0? ¿o eso es implícito?

#R4 
model.addConstr(min[c[p]]*C[p,t] <= c[p,t,e] for t in T_ for e in T_ for p in P_)

#R5
model.addConstrs(i[p,0,e] == 0 for e in T_ for p in P_)

#R6 
model.addConstrs(i[p,t,e] == i[p, t-1, e+1] + c[p,t,e] -s[p,t,e] for t in T_ for e in range(1, T) for p in P_)

#R7
model.addConstrs(i[p,t,T] == c[p,t,T] - s[p,t,T] for t in T_ for p in P_)

#R8 
model.addConstrs(c[p,t,e] == 0 for t in T_ for p in P_ for e in T_ )
#e != exp_p ¿Cómo lo pongo?

#R9 
model.addConstrs(sum(i[p,t-1,e] + c[p,t,e] for e in range(2, T+1)) >= d[p,t] for t in T_ for p in P_)

#R10
model.addConstrs(sum(sum(i[p,t,e]*v[p] for e in range(2,T+1)) for p in P_) <= V[q] for q in Q_ for t in T_) 

#R11 
model.addConstrs(sum(sum(c[p,t,e]*v[p] for e in T_) for p in P_) <= max[c[p]] for p in P_ for t in T_)

#R12 
model.addConstrs(sum(s[p,t,e] for e in T_) == d[p,t] for p in P_ for t in T_)

#R13 
model.addConstrs(w[p,t] == i[p,t,1] for p in P_ for t in T_)

#R14 
model.addConstrs(sum(C[p,t] for t in range(1 + N*7, 7 + N*7 + 1)) <= 1 for p in P_ for N in range(0, T/7))

#R15
model.addConstrs(c[p,t,e] >= 0 for t in T_ for p in P_ for e in T_) 

#R16
model.addConstrs(s[p,t,e] >= 0 for t in T_ for p in P_ for e in T_)  

#R17
model.addConstrs(i[p,t,e] >= 0 for t in T_ for p in P_ for e in T_)  

#R18 
model.addConstrs(w[p,t] >= 0 for t in T_ for p in P_) 

#R19
model.addConstrs(B[t] >= 0 for t in T_) 

#20
#¿No es neceasario la naturaleza de las variables binarias o no?

model.setObjective(objetivo, GRB.MINIMIZE)

model.optimize()

#### Imprimir resultados