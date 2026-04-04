import numpy as np
from tqdm import tqdm
from scipy.spatial import cKDTree
from numba import njit
import write_file as wf
import forces
import Variables_Globales as variables
import numpy.random as rd
import initialize_system as init_sys

#%% IMPORTACION DE VARIABLES GLOBALES
tmax = variables.tmax
numNeigh = variables.numNeigh
dt0 = variables.dt0
dtmin = variables.dtmin
dtmax = variables.dtmax
N = variables.N_cluster
R = variables.R
m = variables.m
epsilon = variables.epsilon
rho0 = variables.rho0
eta = variables.eta
NCM = variables.NCM
rng = rd.default_rng() # Generador de numeros aleatorios
bar_refresh_rate = variables.bar_refresh_rate
neighInfo_refresh_rate = variables.neighInfo_refresh_rate
#%%


@njit(fastmath = True)
def time_variation(acc, dt_current):
    N = len(acc)
    acc2_max = 0.0

    for i in range(N):
        acc2 = acc[i, 0]*acc[i, 0] + acc[i, 1]*acc[i, 1] + acc[i, 2]*acc[i, 2]
        if acc2 > acc2_max:
            acc2_max = acc2

    acc_max = np.sqrt(acc2_max)
    
    if acc_max == 0:
        return dt_current

    dt_target = eta*np.sqrt(epsilon/acc_max)

    if dt_current == None:
        dt_new = dt_target
    elif dt_target > 1.2*dt_current:
        dt_new = 1.2*dt_current
    else:
        dt_new = dt_target

    if dt_new < dtmin:
        dt_new = dtmin
    if dt_new > dtmax:
        dt_new = dtmax

    return dt_new


def Verlet_Iteration(pos, vel, acc, dt, neighInfo, count_for_neighInfo):
    """
    Verlet_Iteration:
    Dada una distribucion de masas en una nube molecular sin condiciones periodicas,
    su cinematica en ese instante de tiempo con el paso variable actual considerando numk vecinos.
    """
    halfVel = vel + 0.5*dt*acc

    rNew = pos + dt*halfVel

    if count_for_neighInfo > neighInfo_refresh_rate:
        new_NeighInfo = forces.Neigh_Function(pos)
        count_for_neighInfo = 0
    else:
        new_NeighInfo = neighInfo
        count_for_neighInfo += 1
    
    accNew = forces.Acceleration_Numba(rNew, halfVel, new_NeighInfo) # No tengo del todo claro que deba ser halfVel, quizas deberia ser vel a secas
    vNew = halfVel + 0.5*dt*accNew                                                      
    
    return rNew, vNew, accNew, new_NeighInfo, count_for_neighInfo


def Temporal_Simulation(r0, v0):
    """
    Dada las condiciones inciales, simula la evolucion de la nube molecular mediante
    un verlet orden 2.
    """
    neighInfo = forces.Neigh_Function(r0) # Neigh distance, neigh Index
    acc0 = forces.Acceleration_Numba(r0,v0, neighInfo)

    dt = time_variation(acc0, dt0)
    t = 0. 
    count = 0
    count_for_neighInfo = 0

    part_time = 0.

    with tqdm(total = tmax) as pbar:
        while t < tmax:

            rNew, vNew, accNew, neighInfo, count_for_neighInfo = Verlet_Iteration(r0, v0, acc0, dt, neighInfo, count_for_neighInfo)

            wf.Pos_To_Txt(rNew, count, dt = dt)
            r0, v0, acc0 = rNew, vNew, accNew

            t += dt
            part_time += dt
            count += 1

            pbar.set_postfix({"dt": f"{dt:.2e}", "N_part": len(r0)})

            dt = time_variation(acc0, dt)
            if part_time >= bar_refresh_rate:
                pbar.update(part_time)
                part_time = 0.
    return



            




    

    



    
    