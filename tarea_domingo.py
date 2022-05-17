from gurobipy import Model, GRB, quicksum
import random


K = 30
n = 12
M = 5
D = 8
S = 2900

#rangos
N_ = range(1, n + 1)
K_ = range(1, K + 1)
M_ = range(1, M + 1)
D_ = range(1, D + 1)

#Conjuntos
G = {(i): random.randint(15000, 40000) for i in N_}
C = {(i, k): random.randint(5000, 10000) for i in N_ for k in K_}
d = {(i, k): random.randint(0, 7) for i in N_ for k in K_}
t = {(i,j): random.randint(9,12) for i in N_ for j in M_}
exp = {(i): random.randint(6,12) for i in N_}
# el 20% de los productos pertenecerán a al subconjunto de productos P, que poseen demanda fija en tienda
P = random.choices(N_, k=int(n*0.2))
Q = {(p): random.randint(3,8) for p in P}
N_sin_P = []
for i in N_:
    if i not in P:
        N_sin_P.append(i)



#### ESCRIBA SU MODELO AQUI ####



m = Model()

#Variables
x = m.addVars(N_,M_,D_,K_, vtype = GRB.BINARY)
y = m.addVars(N_,M_,D_,K_)
f = m.addVars(N_,K_, exp)
z = m.addVars(N_,K_,exp)
r = m.addVars(N_,exp)


#Función Objetivo

objetivo =  sum(sum(sum(G[i]*f[i,k,e]   for e in range(1, exp[i] + 1))    
                                        for k in K_)
                                        for i in N_) +\
            sum(sum(sum(G[p] * r[p,e]   for e in range(1, exp[p] + 1))    
                                        for p in P) 
                                        for k in K_) -\
            sum(sum(sum(sum(C[i,k] * y[i,j,h,k] + S * x[i,j,h,k]    for h in D_) 
                                                                    for j in M_) 
                                                                    for k in K_) 
                                                                    for i in N_)

#R1
m.addConstrs(sum(x[i,j,h,k] for i in N_) <= 1   for j in M_ 
                                                for h in D_ 
                                                for k in K_)

#R2
m.addConstrs(y[i,j,h,k] <= t[i,j] * x[i,j,h,k]  for j in M_ 
                                                for i in N_ 
                                                for k in K_ 
                                                for h in D_)

#R3
m.addConstrs(sum(f[i,k,e] for e in range(1,exp[i] + 1)) == d[i,k]   for i in N_ 
                                                                    for k in K_)

#R4
m.addConstrs(z[i,k,e] == z[i,k-1,e+1] - f[i,k,e]    for i in N_sin_P 
                                                    for e in range(1,exp[i]) 
                                                    for k in range(2,K+1))

#R5
m.addConstrs(sum(sum(y[i,j,h,k] for h in D_) for j in M_) - f[i,k,exp[i]] == z[i,k,exp[i]]  for i in N_sin_P 
                                                                                            for k in K_)
#R6
m.addConstrs(sum(r[p,e] for e in range(1, exp[p] + 1)) == Q[p] for p in P)

#R7
m.addConstrs(z[p,k,e] == z[p,k-1,e+1] - f[p,k,e] - r[p,e]   for p in P 
                                                            for e in range(1,exp[i]) 
                                                            for k in range(2,K+1))

#R8
m.addConstrs(sum(sum(y[p,j,h,k] for h in D_) for j in M_) - f[p,k,exp[p]] - r[p,exp[p]] == z[p,k,exp[p]]    for p in P 
                                                                                                            for k in K_)

#R9
m.addConstrs(z[i,1,e] == 0 for i in N_ 
                           for e in range(1, exp[i]))

#R10
m.addConstrs(x[i,j,h,k] <= y[i,j,h,k]   for i in N_ 
                                        for j in M_ 
                                        for h in D_ 
                                        for k in K_)

m.setObjective(objetivo, GRB.MAXIMIZE)

m.optimize()

#Imprimir Valor Objetivo
print(m.ObjVal) 

