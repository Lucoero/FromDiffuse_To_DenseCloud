import numpy as np
from scipy.spatial import cKDTree
from numba import njit, prange
import Variables_Globales as variables


G = variables.G
m = variables.m
k_dis = variables.k_dis
NCM = variables.NCM
h = variables.h
A = variables.A


def Numpy_Distances(r, neigh):
    neighDist, neighIndex = neigh

    rNeigh = r[neighIndex]
    r_3dim = r[:, np.newaxis, :]

    r_np = rNeigh - r_3dim
    r_np = r_np[:, 1:, :]

    mod = neighDist[:, 1:]
    mod_np = mod[:, :, np.newaxis]

    return r_np, mod_np

def Acceleration_Numpy(r, neigh):
    '''
    Acceleration_Numpy: 
    Calculamos la fuerza gravitatoria que recibe cada particula por sus vecinos (forma vectorizada, usandose numpy)
    
    Parametros de entrada:
    r: La matriz (N, 3) con las posiciones de todas las particulas
    neigh: Tupla con las distancias de los k-primeros vecinos y sus indices. Ambas matrices
    
    Parametros de salida:
    acc: Matriz (N,3) de la aceleracion total que sufre cada particula
    '''
    k_grav = G*m # La k no necesita -, el vector director lo lleva implicito. Solo multiplico por m porque es la aceleracion

    neighDist, neighIndex = neigh
    rNeigh = r[neighIndex]
    r_3dim = r[:, np.newaxis, :]

    r_np = rNeigh - r_3dim
    r_np = r_np[:, 1:, :]

    mod = neighDist[:, 1:]
    mod_np = mod[:, :, np.newaxis]

    acc_nps_grav = k_grav * (r_np/mod_np**3)
    acc = np.sum(acc_nps_grav, axis = 1)

    return acc

@njit(parallel = True, fastmath = True)
def Acceleration_Numba_CM_disipativa_provisional(r, v, neigh, indexCM):
    '''
    Acceleration_Numba:
        Dado r en matrices (N,3), devuelve la aceleracion que sufren dichas particulas mediante Numba
        debido a diferentes fuerzas: Fuerza gravitatoria, fuerza de arrastre y leve fuerza de repulsion a lo Lennard
        
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

    accSum = np.zeros(3) # La suma de todas las aceleraciones. Para el compensado del CM
    NCM = len(indexCM)
    
    for i in prange(N):
        
        if i in indexCM: # A esta no le calculamos la aceleracion
            #print(i)
            continue
        
        # Calculamos el vector director para la fuerza disipativa (que es en la direccion de la velocidad)
        vxx = v[i,0]*v[i,0] 
        vyy = v[i,1]*v[i,1]
        vzz = v[i,2]*v[i,2]
        vmod2 = vxx + vyy + vzz
        v_dirx = vxx/vmod2
        v_diry = vyy/vmod2
        v_dirz = vzz/vmod2
    
        for j in range(num_k):
            if neighIndex[i, j] == i: # Para quitarnos la interaccion de una particula consigo misma
                continue
            r_npx = r[neighIndex[i,j], 0] - r[i, 0]
            r_npy = r[neighIndex[i,j], 1] - r[i, 1]
            r_npz = r[neighIndex[i,j], 2] - r[i, 2]

            r2 = r_npx*r_npx + r_npy*r_npy + r_npz*r_npz
            mod_np = r2**0.5

            # Seccion fuerza gravitatoria:
            mod_np3 = mod_np**3
            # No la sumes a la aceleracion total si la vamos a usar para compensar CM
            acc[i, 0] += k_grav * (r_npx/mod_np3)
            acc[i, 1] += k_grav * (r_npy/mod_np3)
            acc[i, 2] += k_grav * (r_npz/mod_np3)
            #print("accGrav:", acc[i,0])
            # Seccion fuerza de repulsion/presion:
            
            expon = np.exp(-mod_np/h)
            
            acc[i,0] += A*r_npx*expon/(m*mod_np)
            acc[i,1] += A*r_npy*expon/(m*mod_np)
            acc[i,2] += A*r_npz*expon/(m*mod_np)
            
            # Seccion fuerza disipativa:
                
            #gamma = np.exp(-k_dis*mod_np)/m # Metemos la masa aqui para ahorrarnos calculos y coste computacional
            #gamma = k_dis/mod_np/m
            gamma = k_dis
        
            v_npx = v[neighIndex[i, j], 0] - v[i, 0] # incluye el menos de v1-v2 implicito
            v_npy = v[neighIndex[i, j], 1] - v[i, 1]
            v_npz = v[neighIndex[i, j], 2] - v[i, 2]
    
            acc[i, 0] += gamma * v_npx # * v_dirx
            acc[i, 1] += gamma * v_npy # * v_diry
            acc[i, 2] += gamma * v_npz # * v_dirz
            #print("accDis + Grav:", acc[i,0])
           
    
        # Finalmente, metemos la aceleracion calculada a la suma
        accSum[0] += acc[i,0]
        accSum[1] += acc[i,1]
        accSum[2] += acc[i,2]
        
    # Antes de returnear, cambio la acc necesaria para compensar Vel CM
    #print("aceleracion de compensacion x", accSum[2])
    
    accSum[0] = accSum[0]/NCM
    accSum[1] = accSum[1]/NCM
    accSum[2] = accSum[2]/NCM
    for k in indexCM:
        acc[k,0] = - accSum[0]
        acc[k,1] = - accSum[1]
        acc[k,2] = - accSum[2]
    return acc

def Temporal_Simulation_descartada(r0, v0):
    """
    Dada las condiciones inciales, simula la evolucion de la nube molecular mediante
    un verlet orden 2.
    """
    indexCM = np.arange(0,NCM,1)  # Unico de no Variables_Globales porque lo vamos a meter en Numba y es mas eficiente asi (creo)
    neighInfo = forces.Neigh_Function(r0) # Neigh distance, neigh Index
    acc0 = forces.Acceleration_Numba(r0,v0, neighInfo, indexCM = indexCM)
    indexCM = rng.integers(0,N, size = NCM)
    n = int(np.round(tmax/dt0)) + 1
    for i in tqdm(range(1, n)):
        rNew, vNew, accNew = Verlet_Iteration(r0, v0, acc0, dt0, indexForCM = indexCM)

        wf.Pos_To_Txt(rNew, i, dt = dt0)
        r0, v0, acc0 = rNew, vNew, accNew
    
        # Escojo aleatoriamente una nueva particula para compensar el CM
        #VCM = np.sum(v0)/N
        #print(VCM)
        indexCM = rng.integers(0,N,size = NCM)
    return 





