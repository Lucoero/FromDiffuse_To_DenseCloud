import numpy as np
from scipy.spatial import cKDTree
from numba import njit, prange
import Variables_Globales as variables


# IMPORTACION DE VARIABLES GLOBALES
m = variables.m
G = variables.G
numNeigh = variables.numNeigh
k_dis = variables.k_dis
h = variables.h
A = variables.A

def Neigh_Function(r):
    '''
    Neigh_Function: funcion para la obtencion de los vecinos de una particula
    
    :param r: posiciones de las particulas (N, 3)
    :param num_k: Numero de vecinos deseado, sin contar a la propia particula.
    '''
    tree = cKDTree(r)

    neighDistance, neighIndex = tree.query(r, (numNeigh + 1)) # Tomamos k + 1 porque 1 de ellos siempre va a ser ella misma
                                                           # Cuando no existe el suficiente numero de vecinos lo que hace es añadir inf en ciertas posiciones
    return neighDistance, neighIndex


@njit(parallel = True, fastmath = True)
def Acceleration_Numba(r,v, neigh):
    '''
    Acceleration_Numba:
        Dado r en matrices (N,3), devuelve la aceleracion que sufren dichas
        particulas mediante Numba
        debido a diferentes fuerzas: Fuerza gravitatoria, 
        fuerza de arrastre y leve fuerza de repulsion a lo Lennard
        
        Parametros entrada:
            r: Matriz (N,3) de posiciones
            neigh: Tupla de Distancia de Vecinos, Indices de vecinos
            indexCM: Array de indices de las particulas que van a compensar
        Salida:
            acc: Matriz (N,3) de la aceleracion total que sufre cada particula.
    '''

    k_grav = G*m # La k no necesita -, el vector director lo lleva implicito
    neighIndex = neigh[1]
    N = len(r)
    num_k = len(neighIndex[0])

    acc = np.zeros((N, 3), dtype = np.float64) 
    
    for i in prange(N):

        for j in range(num_k):
            if neighIndex[i, j] == i: # No interaccion de una particula consigo misma
                continue
            r_npx = r[neighIndex[i,j], 0] - r[i, 0]
            r_npy = r[neighIndex[i,j], 1] - r[i, 1]
            r_npz = r[neighIndex[i,j], 2] - r[i, 2]

            r2 = r_npx*r_npx + r_npy*r_npy + r_npz*r_npz
            mod_np = r2**0.5

            errcorr = 0.001 # Para evitar error div0
            denom = m*mod_np + errcorr 

            denom2 = m*(mod_np*mod_np)
            denom2 = denom2 + errcorr
            # Seccion fuerza gravitatoria:
            mod_np3 = mod_np**3
            mod_np3 = mod_np3 + errcorr
            acc[i, 0] += k_grav * r_npx/mod_np3
            acc[i, 1] += k_grav * r_npy/mod_np3
            acc[i, 2] += k_grav * r_npz/mod_np3
            
            # Seccion fuerza de repulsion/presion:
            # OJO: En el paper de Larrson consieran que la aceleracion 
            # de repulsion es de la forma c**2/r (en la direccion radial)
            # expon = np.exp(-mod_np/h) 
            acc[i,0] -= A*r_npx/denom2 # *expon
            acc[i,1] -= A*r_npy/denom2 # *expon
            acc[i,2] -= A*r_npz/denom2 # *expon
            
            # Seccion fuerza disipativa:
            # incluye el menos de v1-v2 implicito
            v_npx = v[neighIndex[i, j], 0] - v[i, 0] 
            v_npy = v[neighIndex[i, j], 1] - v[i, 1]
            v_npz = v[neighIndex[i, j], 2] - v[i, 2]

            vDotr = v_npx*r_npx + v_npy*r_npy + v_npz*r_npz
            # El angulo entre v y r esta en el segundo o tercer cuadrante (se alejan) si vDot r < 0 
            if vDotr > 0: 
                gamma = k_dis

                acc[i, 0] += gamma * v_npx
                acc[i, 1] += gamma * v_npy
                acc[i, 2] += gamma * v_npz
    return acc
